from aiogram import types, Dispatcher
from bot import dp, bot
from scraper.scraper import Scraper
# import asyncio
from database.db import get_session
from database.models.Users import Users

scraper = Scraper()
session = get_session()

# async def timer_func(message):
#     for i in range(1):
#        await message.answer(f"Starting scraping!{i}")
#        await asyncio.sleep(1) 
#     return True

async def start_command(message: types.Message):
    # await timer_func(message)
    with session:
        user_in_db = session.query(Users).filter(Users.tg_id == message.from_user.id).first()
        if not user_in_db:
            user = Users(message.from_user.first_name, message.from_user.username, message.from_user.id, message.chat.id, "user")
            session.add(user)
            session.commit()
    try:
        await bot.send_message(message.from_user.id, "Hello world!")
    except:
        await message.reply('Find me here! \n t.me/ai_course_test_bot')


def register_user_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])  


