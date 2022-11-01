""""Проверка id - пропускаем сообщение только от одного пользователя"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):

    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def id_check(self, message: types.Message):
        if int(message.from_user.id) != int(self.access_id):
            await message.answer(text="Access denied")
            raise CancelHandler()
