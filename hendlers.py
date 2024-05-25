from aiogram import types
from aiogram.dispatcher import FSMContext
from templates.states import Form
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'token'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Пример занятых и свободных дат и времени
busy_dates = ["2024-05-26", "2024-05-27"]
free_dates = ["2024-05-28", "2024-05-29"]
busy_times = ["10:00", "14:00"]
free_times = ["12:00", "16:00"]

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.fio.set()
    await message.reply("Введите ваше ФИО:")

@dp.message_handler(state=Form.fio)
async def process_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await Form.next()
    await message.reply("Выберите врача (например, Терапевт, Хирург):")

@dp.message_handler(state=Form.doctor)
async def process_doctor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['doctor'] = message.text
    await Form.next()
    await message.reply("Выберите дату из доступных:\n" +
                        f"Свободные даты: {', '.join(free_dates)}\n" +
                        f"Занятые даты: {', '.join(busy_dates)}")

@dp.message_handler(state=Form.date)
async def process_date(message: types.Message, state: FSMContext):
    chosen_date = message.text

    # Проверяем, свободна ли выбранная дата
    if chosen_date in busy_dates:
        await message.reply("Выбранная дата уже занята. Пожалуйста, выберите другую дату.")
    elif chosen_date not in free_dates:
        await message.reply("Неверная дата. Пожалуйста, выберите дату из доступных.")
    else:
        async with state.proxy() as data:
            data['date'] = chosen_date
        await Form.next()
        await message.reply("Выберите время из доступных: " + ', '.join(free_times))

@dp.message_handler(state=Form.time)
async def process_time(message: types.Message, state: FSMContext):
    chosen_time = message.text

    # Проверяем, свободно ли выбранное время
    if chosen_time in busy_times:
        await message.reply("Выбранное время уже занято. Пожалуйста, выберите другое время.")
    elif chosen_time not in free_times:
        await message.reply("Неверное время. Пожалуйста, выберите время из доступных.")
    else:
        async with state.proxy() as data:
            data['time'] = chosen_time

            # Здесь можно добавить логику сохранения информации о записи в базу данных
            appointment_info = (
                f"ФИО: {data['fio']}\n"
                f"Врач: {data['doctor']}\n"
                f"Дата: {data['date']}\n"
                f"Время: {data['time']}"
            )
            await message.reply(f"Запись завершена:\n{appointment_info}")

        await state.finish()

from aiogram import executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)