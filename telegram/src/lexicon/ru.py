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
}
