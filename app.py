from aiogram import executor
from bot import dp
from handlers import user_main

async def on_startup(_):
    print("Bot started!")

user_main.register_user_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


