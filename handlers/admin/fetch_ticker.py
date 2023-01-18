from aiogram import types, Dispatcher
from bot import bot
import asyncio
from utils.helpers.helpers import is_admin
from database.models.Ticker_ETHUSDT_15m import Ticker_ETHUSDT_15m
from utils.fetcher.fetch_ticker import Fetch_ticker

ticker = Fetch_ticker()

async def fetch_ticker_command(message: types.Message):
    if is_admin(message):
        m = await bot.send_message(message.from_user.id, "Working...")
        com = message.text.split()
        if len(com) == 2:
            if com[1] == "ETHUSDT":
                await asyncio.get_running_loop().run_in_executor(None, ticker.fetch_ticker, Ticker_ETHUSDT_15m, 1661352300000)
                await m.edit_text("Job finished!")
            elif com[1] == "BTCUSDT":
                await m.edit_text("Not available yet!")
                # await asyncio.get_running_loop().run_in_executor(None, ticker.fetch_ticker, Ticker_ETHUSDT_15m, 1661352300000)
            else:
                await m.edit_text("Wrong command!")
        else:
            await m.edit_text("Wrong command!")
    else:
        await bot.send_message(message.from_user.id, "Only admin can use this command!")
    

def register_user_fetc_ticker_handlers(dp: Dispatcher):
    dp.register_message_handler(fetch_ticker_command, commands=['fetch_ticker'])
