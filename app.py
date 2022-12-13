from aiogram import executor
import asyncio
from bot import dp
from handlers import user_main
from database.db import engine
from database.orm_base import metadata
from utils.scheduler import scheduler


async def on_startup(_):
    print("Bot started!")
    print("Starting database!")
    metadata.create_all(bind=engine)
    print("Database started!")
    asyncio.create_task(scheduler())
    print("Schedulers loaded!")

    
    
    


user_main.register_user_handlers(dp)





executor.start_polling(dp, skip_updates=False, on_startup=on_startup)


