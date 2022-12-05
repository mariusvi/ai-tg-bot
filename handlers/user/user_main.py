from aiogram import types, Dispatcher
from bot import dp, bot

async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Hello world")
    except:
        await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def about_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Here is about text! bot.send")
    await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def text_command(message: types.Message):
    await message.answer("Here is about text! message.answer")

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])  
    dp.register_message_handler(about_command, commands=['about'])
    dp.register_message_handler(text_command, commands=['text'])


