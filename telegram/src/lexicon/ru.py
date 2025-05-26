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
}
