from aiogram import types, Dispatcher
from src.bot import bot
from database.db import get_session
from database.models.Users import Users
import asyncio

session = get_session()


async def timer_func(message):
    for i in range(10):
        #    await message.answer(f"Starting scraping!{i}")
        await asyncio.sleep(2)
        print("bla")
    return True


async def db_command(message: types.Message):
    await timer_func(message=message)
    with session:
        user = Users("test name", "test tg user name", 1231, 9874, "user")
        session.add(user)
        session.commit()
    await bot.send_message(message.from_user.id, "Data in database!")


def register_user_test_db_handlers(dp: Dispatcher):
    dp.register_message_handler(db_command, commands=["test_db"])
