from aiogram import types, Dispatcher
from bot import dp, bot
from scraper.scraper import Scraper
# import asyncio
from database.db import get_session
from database.models.Users import Users
from database.models.Data_sources import Data_sources
from datetime import datetime


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

async def about_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Here is about text!")
    await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def scrape_command(message: types.Message):
    before = datetime.now()
    await message.answer("Start scraping!")
    data = await scraper.scrape('', ['crypto'])
    with session:
        for scraper_data in data:
            for item in scraper_data["items"]:
                if not session.query(Data_sources).filter(Data_sources.name == item.title).first():
                    payload = Data_sources(name = item.title, category=item.category, url=item.url, description=item.description, icon=item.icon)
                    session.add(payload)
                    session.commit()
    result = datetime.now() - before
    await message.answer(f"Job finished! Total time: {result}")

async def db_command(message: types.Message):
    with session:
        user = Users("first name", "tg user name", 1231, 9874, "user")
        session.add(user)
        session.commit()
    await bot.send_message(message.from_user.id, "Data in database!")




def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])  
    dp.register_message_handler(about_command, commands=['about'])
    dp.register_message_handler(scrape_command, commands=['scrape'])
    dp.register_message_handler(db_command, commands=['db'])


