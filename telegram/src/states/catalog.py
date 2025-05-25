from aiogram.filters.state import State, StatesGroup


class FSMCatalog(StatesGroup):
    choose_category = State()
