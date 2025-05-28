"""The module responsible for the handlers for viewing shopping cart."""

from logging import getLogger
from typing import Optional
from uuid import uuid4

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.models.product import Product
from telegram.src.db.queries.product_shopping_cart import (
    remove_product_from_shopping_cart,
)
from telegram.src.db.queries.products import get_product_by_id
from telegram.src.keyboards import SHOPPING_CART_CB
from telegram.src.keyboards.shopping_cart import (
    build_kb_to_buy_product_from_cart,
)
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.products import send_product
from telegram.src.services.shopping_cart import view_shopping_cart
from telegram.src.states.buying_product import FSMBuying

logger = getLogger("telegram.handlers.shopping_cart")
router: Router = Router()


@router.callback_query(F.data == SHOPPING_CART_CB)
async def view_shopping_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """View shopping cart."""
    await view_shopping_cart(
        bot=cb.bot, Session=Session, user_id=cb.from_user.id, config=config
    )


# cb data format is shopping_cart|pagination:page={page}
@router.callback_query(F.data.startswith("shopping_cart|pagination:page="))
async def pagination_shopping_cart(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """Show the product page in the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    page: int = int(cb_data.split("=")[1])
    await view_shopping_cart(
        bot=cb.bot,
        Session=Session,
        user_id=cb.from_user.id,
        config=config,
        page=page,
    )


# cb data format is shopping_cart|view_product:product_id={product_id};count={count}
@router.callback_query(
    F.data.startswith("shopping_cart|view_product:product_id=")
)
async def buy_product_from_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
):
    """Show a detailed product page from the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    product_id_data, count_data = cb_data.split(";")
    product_id, count = int(product_id_data.split("=")[1]), int(
        count_data.split("=")[1]
    )
    product: Optional[Product] = await get_product_by_id(Session, product_id)

    if product is None:
        await cb.bot.send_message(
            chat_id=cb.from_user.id, text=LEXICON_RU["product_not_found"]
        )
    else:
        await send_product(
            cb,
            product,
            inline_kb=build_kb_to_buy_product_from_cart(product_id, count),
        )


# shopping_cart|remove:product_id={product_id}
@router.callback_query(F.data.startswith("shopping_cart|remove:product_id="))
async def remove_product_from_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """Remove product from the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    product_id = int(cb_data.split("=")[1])
    record_was_exist: bool = await remove_product_from_shopping_cart(
        Session, cb.from_user.id, product_id
    )
    if record_was_exist:
        await view_shopping_cart_handler(cb, Session, config)


# shopping_cart|order:product_id={product_id};count={count}
@router.callback_query(F.data.startswith("shopping_cart|order:product_id="))
async def start_buying(
    cb: CallbackQuery,
    state: FSMContext,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
) -> None:
    """Start processing payment."""
    # clear state data
    await state.clear()
    await state.set_state(FSMBuying.buying)

    cb_data: str = cb.data.split(":")[1]
    product_id_str, count_str = cb_data.split(";")
    product_id, count = int(product_id_str.split("=")[1]), int(
        count_str.split("=")[1]
    )

    # check that product exists
    product: Optional[Product] = await get_product_by_id(Session, product_id)
    if not product:
        await cb.bot.send_message(
            cb.from_user.id, LEXICON_RU["product_not_found"]
        )
    else:
        if "TEST" in config.ukassa.api_key:
            await cb.bot.send_message(
                cb.from_user.id, text=LEXICON_RU["test_payment"]
            )

        prices = [
            LabeledPrice(
                label=LEXICON_RU["labeled_price_label"].format(
                    name=product.name,
                    price=product.price,
                    count=count,
                ),
                amount=int(product.price * count * 100),  # в копейках
            )
        ]

        await cb.bot.send_invoice(
            chat_id=cb.from_user.id,
            title=product.name[:32],
            description=product.description[:255],
            payload=str(uuid4()),
            currency=config.ukassa.currency,
            provider_token=config.ukassa.api_key,
            prices=prices,
            need_shipping_address=True,
            is_flexible=False,
        )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Process precheckout query."""
    await pre_checkout_query.answer(True)


@router.message(F.successful_payment)
async def process_successful_payment(msg: Message, state: FSMContext):
    """Process successful payment."""
    await msg.reply(
        text=LEXICON_RU["successful_payment"].format(
            address=msg.successful_payment.order_info.shipping_address
        )
    )
    logger.info("Successful payment from user %s", msg.from_user.id)
    await state.clear()


@router.message(StateFilter(FSMBuying.buying))
async def process_unsuccessful_payment(msg: Message, state: FSMContext):
    """Process unsuccessful payment."""
    await msg.reply(LEXICON_RU["unsuccessful_payment"])
    await state.clear()
    logger.info("Unsuccessful payment from user %s", msg.from_user.id)
