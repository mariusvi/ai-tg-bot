from aiogram import executor
from bot import dp
from handlers import user_main
from database import db


async def on_startup(_):
    print("Bot started!")
    print("Starting database!")
    db.start_database()
    print("Database started!")
    
    
    


user_main.register_user_handlers(dp)





executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


