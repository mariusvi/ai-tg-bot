from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
import os

load_dotenv('.env')
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

