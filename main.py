from aiogram import Bot, Dispatcher, types, executor
import os
import logging
from aiogram.dispatcher.handler import CancelHandler


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
ACCESS_ID = int(os.getenv('TELEGRAM_ACCESS_ID'))
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


HELP_MESSAGE = """Добавить расход: сумма_категория (Пример: 100 магазин)\n
                Месячный план трат: _\n
                Траты за сегодня: /today\n
                Траты за текущий месяц: /month\n
                Последние внесенные расходы: /lexpenses\n
                Категории трат: /categories\n"""


def auth(func):
    async def wrapper(message):
        if int(message.from_user.id) != ACCESS_ID:
            await message.answer(text="Access denied")
            raise CancelHandler()
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start'])
@auth
async def welcome_message(message: types.Message):                  #Отправляет приветственное сообщение
    await message.answer(text="Привет, я бот для учета финансов")
    await message.delete()


@dp.message_handler(commands=['help'])
@auth
async def help_message(message: types.Message):        #Отправляет сообщение с функциями бота
    await message.reply(text=HELP_MESSAGE)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)