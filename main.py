from aiogram import Bot, Dispatcher, types, executor
import os
import logging
from aiogram.dispatcher.handler import CancelHandler
from expences import fetch_today_exp, fetch_month_exp, fetch_last_exp, fetch_today_summ, fetch_month_summ
from db import insert, delete
from categories import show_categ_list
from config import api_token, access_id


logging.basicConfig(level=logging.INFO)

API_TOKEN = api_token
ACCESS_ID = int(access_id)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WELCOME_MESSAGE = """Привет, я бот для учета финансов\n
Введите /help для просмотра основных команд\n"""

HELP_MESSAGE = """Добавить расход: сумма_категория (Пример: 100 магазин)\n
Месячный план трат: /plan\n
Траты за сегодня: /today\n
Траты за текущий месяц: /month\n
Последние внесенные расходы: /lexp\n
Категории трат: /categories\n
Удалить последнюю запись: /del\n"""


ERROR_MESSAGE = """Данные не внесены\n
Введите данные по образцу: сумма_категория\n
(Пример: 100 магазин)\n"""


def auth(func):                     #Декоратор для работы бота только с одним аккаунтом
    async def wrapper(message):
        if int(message.from_user.id) != ACCESS_ID:
            await message.answer(text="Иди нахуй путник")
            raise CancelHandler()
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start'])
@auth
async def welcome_message(message: types.Message):                  #Отправляет приветственное сообщение
    await message.answer(text=WELCOME_MESSAGE)
    await message.delete()


@dp.message_handler(commands=['help'])
@auth
async def help_message(message: types.Message):        #Отправляет сообщение с функциями бота
    await message.reply(text=HELP_MESSAGE)
    await message.delete()


@dp.message_handler(commands=['plan'])
@auth
async def show_plan():
    pass


@dp.message_handler(commands=['today'])
@auth
async def show_today_exp(message: types.Message):
    today_exp = [f"{category} - {summa} руб.\n" for x in fetch_today_exp() for category, summa in x.items()]
    today_sum = fetch_today_summ()[0][0]
    answer = 'Траты за сегодня составили:\n\n' + '\n'.join(today_exp) + f'\n\n* Всего за сегодня: {today_sum} руб. *'
    await message.answer(answer)


@dp.message_handler(commands=['month'])
@auth
async def show_month_exp(message: types.Message):
    month_exp = [f"{category} - {summa} руб.\n" for x in fetch_month_exp() for category, summa in x.items()]
    month_sum = fetch_month_summ()[0][0]
    answer = 'Траты в этом месяце составили:\n\n' + '\n'.join(month_exp) + f'\n\n* Всего за месяц: {month_sum} руб. *'
    await message.answer(answer)


@dp.message_handler(commands=['lexp'])
@auth
async def show_last_exp(message: types.Message):
    last_exp = [f"{category} - {summa} руб.\n" for x in fetch_last_exp() for category, summa in x.items()]
    answer = 'Последняя трата:\n\n' + ''.join(last_exp)
    await message.answer(answer)


@dp.message_handler(commands=['categories'])
@auth
async def show_categories(message: types.Message):
    categ_list = [f"{x}\n" for x in show_categ_list()]
    answer = 'Список категорий:\n\n' + ''.join(categ_list)
    await  message.answer(answer)


@dp.message_handler(commands=['del'])
@auth
async def delete_message(message: types.Message):
    await message.answer(delete())


@dp.message_handler()
@auth
async def insert_message(message: types.Message):
    try:
        await message.reply(insert(message.text, message.date))
    except ValueError or IndexError:
        await message.reply(text=ERROR_MESSAGE)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
