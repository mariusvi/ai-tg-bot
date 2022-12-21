from aiogram import executor
import asyncio
from bot import dp
from handlers import start
from handlers import about
from handlers import test_db
from handlers import scrape
from handlers import fetch_blocks
from database.db import engine
from database.orm_base import metadata
from utils.scheduler.scheduler import scheduler


async def on_startup(_):
    print("Bot started!")
    print("Starting database!")
    metadata.create_all(bind=engine)
    print("Database started!")
    asyncio.create_task(scheduler())
    print("Schedulers loaded!")

scrape.register_admin_scrape_handlers(dp)
start.register_user_start_handlers(dp)
about.register_user_about_handlers(dp)
test_db.register_user_test_db_handlers(dp)
fetch_blocks.register_user_fetc_blocks_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


