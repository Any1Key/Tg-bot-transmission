from aiogram.fsm.state import State, StatesGroup


class AddDirState(StatesGroup):
    name = State()
    path = State()
