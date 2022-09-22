from aiogram.dispatcher.filters.state import StatesGroup, State

class MenuState(StatesGroup):
    TYPE = State()
    GROUP = State()
    ITEM = State()