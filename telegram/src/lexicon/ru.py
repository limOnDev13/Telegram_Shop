"""The module responsible for the Russian lexicon."""

from typing import Dict

LEXICON_RU: Dict[str, str] = {
    "start": "Приветствую!",
    "subscription_verification": "Проверяю подписку на каналы...",
    "failed_subscription_verification": "Вы не подписаны на эти каналы. "
    "Подпишитесь и снова вызовете команду /start.",
    "successful_subscription_verification": "Главное меню",
    "catalog_bt": "Каталог",
    "shopping_cart_bt": "Корзина",
    "faq_bt": "FAQ",
    "catalog": "Категории:",
    "back_bt": "<",
    "next_bt": ">",
    "cur_page_bt": "{page}/{pages}",
    "back_to_main_menu_bt": "ГЛАВНОЕ МЕНЮ",
    "product": "<b>{name}</b>\n\n{description}",
    "next_batch_bt": "Еще",
    "buy_button": "Добавить в корзину {name} ({price})",
    "how_many_products": "Сколько желаете приобрести?",
    "wrong_input_while_buying_product": "Пожалуйста, "
    "введите положительное целое число.",
    "product_in_sc": "{name} ({price}) | {count} шт | Всего: {total}",
    "shopping_cart": "Ваша корзина",
    "buy_product_bt": "Купить",
    "remove_from_cart": "Удалить из корзины",
    "product_not_found": "Упс... Товар не найден!",
}
