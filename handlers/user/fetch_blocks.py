from aiogram import types, Dispatcher
from bot import bot
from database.db import get_session
from utils.fetcher.fetch_blocks import Fetch_blocks
import asyncio

session = get_session()
fetcher = Fetch_blocks(1)

async def fetch_blocks(message: types.Message):
    m = await bot.send_message(message.from_user.id, "Working...")
    com = message.text.split()
    if len(com) == 1:
        time = await asyncio.get_running_loop().run_in_executor(None, fetcher.start_fetch, [])  
        await m.edit_text(f"Fetch job finished in {round(time, 3)} seconds")
    elif len(com) == 2:
        await m.edit_text("Wrong command! START and END blocks required")
    elif len(com) == 3:
        time = await asyncio.get_running_loop().run_in_executor(None, fetcher.start_fetch, [int(com[1]), int(com[2])])  
        await m.edit_text(f"Fetch job finished in {round(time, 3)} seconds")
    else:
        await m.edit_text("Wrong command!")
    
   

def register_user_fetc_blocks_handlers(dp: Dispatcher):
    dp.register_message_handler(fetch_blocks, commands=['fetch'])