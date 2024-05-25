from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    fio = State()
    doctor = State()
    date = State()
    time = State()