"""The package responsible for the handlers of the bot."""

from .catalog import router as catalog_router
from .products import router as product_router
from .shopping_cart import router as shopping_cart_router
from .start_conversation import router as start_conversation_router
