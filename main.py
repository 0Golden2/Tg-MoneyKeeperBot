from aiogram import Bot, Dispatcher, types
import os


API_TOKEN = os.getenv('5466461965:AAGlL5aTei7QVRiQ6d55ys1rwx74gfY-pHE')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome_message(message: types.Message):
    """Отправляет приветственное сообщение"""
    await message.answer(
        "Привет, я бот для учета финансов\n\n"
        "Добавить расход: сумма_категория (Пример: 100 магазин)\n"
        "Месячный план трат: _\n"
        "Траты за сегодня: /today\n"
        "Траты за текущий месяц: /month\n"
        "Последние внесенные расходы: /lexpenses\n"
        "Категории трат: /categories\n"
    )
