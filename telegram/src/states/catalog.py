"""The module responsible for checking the status when viewing the catalog."""

from aiogram.filters.state import State, StatesGroup


class FSMCatalog(StatesGroup):
    """FSM for viewing categories."""

    choose_category = State()
    view_products = State()
