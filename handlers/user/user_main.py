from aiogram import types, Dispatcher
from bot import dp, bot
from scraper.scraper import Scraper
import asyncio
from datetime import datetime

scraper = Scraper()

async def timer_func(message):
    for i in range(1):
       await message.answer(f"Starting scraping!{i}")
       await asyncio.sleep(1) 
    return True

async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Hello world")
    except:
        await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def about_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Here is about text! bot.send")
    await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def scrape_command(message: types.Message):
    before = datetime.now()
    await message.answer("Starting scraping!")
    # await timer_func(message)
    data = await scraper.scrape('', ['crypto'])
    # do something with data: to SQL.....
    result = datetime.now() - before
    await message.answer(f"Job finished! Total time: {result}")


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])  
    dp.register_message_handler(about_command, commands=['about'])
    dp.register_message_handler(scrape_command, commands=['scrape'])


