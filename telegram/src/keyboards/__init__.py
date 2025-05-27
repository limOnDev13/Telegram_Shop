"""The package responsible for the keyboard of the bot."""

CATEGORY_CB: str = "category"
CATEGORY_PAGINATION: str = (
    "category:page={page};category_id={category_id};path={path}"
)
CATEGORY_CUR_PAGE_CALLBACK: str = "category:cur_page"
BACK_TO_MAIN_MENU_CALLBACK: str = "back_to_main_menu"
PRODUCT_CB: str = "product:category_id={category_id}"
BUY_PRODUCT_CB: str = "product|buy:product_id={product_id}"
SHOPPING_CART_CB: str = "shopping_cart"
SHOPPING_CART_BUY_PRODUCT_CB: str = (
    "shopping_cart|view_product:product_id={product_id};count={count}"
)
SHOPPING_CART_PAGINATION_CB: str = "shopping_cart|pagination:page={page}"
SHOPPING_CART_CUR_PAGE_CB: str = "shopping_cart|current_page"
SHOPPING_CART_REMOVE_PRODUCT_CB: str = (
    "shopping_cart|remove:product_id={product_id}"
)
SHOPPING_CART_MAKING_ORDER: str = (
    "shopping_cart|order:product_id={product_id};count={count};user_id={user_id}"
)
