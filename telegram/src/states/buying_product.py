"""The module responsible for the purchase states."""

from aiogram.filters.state import State, StatesGroup


class FSMBuying(StatesGroup):
    """FSM for buying process."""

    buying = State()
