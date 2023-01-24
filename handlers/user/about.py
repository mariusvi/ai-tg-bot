from aiogram import types, Dispatcher
from src.bot import dp, bot


async def about_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Here is about text!")
    await message.reply("Find me here! \n t.me/ai_course_test_bot")


def register_user_about_handlers(dp: Dispatcher):
    dp.register_message_handler(about_command, commands=["about"])
