import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

# Загружаем токены из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Создаем объекты bot и dp
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Learning(StatesGroup):
    waiting_for_subject = State()
    waiting_for_iterations = State()


@dp.message_handler(Command("start"), state=None)
async def start_command(message: types.Message):
    await message.answer("Привет! Какая тема обучения?")
    await Learning.waiting_for_subject.set()


@dp.message_handler(state=Learning.waiting_for_subject)
async def learning_subject_chosen(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    keyboard.add(*buttons)
    await message.answer("Сколько итераций должно быть обучения?", reply_markup=keyboard)
    await Learning.waiting_for_iterations.set()


@dp.message_handler(state=Learning.waiting_for_iterations)
async def learning_iterations_chosen(message: types.Message, state: FSMContext):
    await state.update_data(iterations=int(message.text))
    await message.answer("Начинаем обучение...", reply_markup=types.ReplyKeyboardRemove())
    await start_learning_cycle(message, state)


async def start_learning_cycle(message: types.Message, state: FSMContext):
    import src.FeinmanLearning as FL
    data = await state.get_data()
    subject = data.get("subject")
    fl = FL.FeynmanLearning(subject,subject)
    iterations = data.get("iterations")

    for i in range(iterations):
        # Шаг 2: обучение
        fl.set_step(2)
        learning_text = fl.generate_answer()
        await message.answer(learning_text)

        # Шаг 3: уточнение данных
        fl.set_step(3)
        refining_text = fl.generate_answer()
        await message.answer(refining_text)

    # Шаг 4: обобщение
    fl.set_step(4)
    summary_text = fl.generate_answer()
    await message.answer(summary_text)
    await message.answer("Обучение завершено!")
    await state.finish()


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)