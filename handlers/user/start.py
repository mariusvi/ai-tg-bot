from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import dp, bot
from scraper.scraper import Scraper
# import asyncio
from database.db import get_session
from database.models.Users import Users

scraper = Scraper()
session = get_session()

BANNER = "https://cdn.dribbble.com/users/1373613/screenshots/5385718/media/30cede328265c92d61aa211591e70b62.gif"

START_CAPTION = """<b>Hi!!</b>

<em>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus 
tempor tristique sagittis. Mauris imperdiet imperdiet enim vel efficitur. 

Fusce elementum sem quis mauris pulvinar, eu tincidunt leo viverra.
</em>"""
commands_button = InlineKeyboardButton(text="📖 Commands", callback_data="COMMANDS_BUTTON")
datasets_button = InlineKeyboardButton(text="🔢 Database", callback_data="DATABASE_BUTTON")
predictions_button = InlineKeyboardButton(text="🎯 Predictions", callback_data="PREDICTIONS_BUTTON")
START_KEYBOARD = InlineKeyboardMarkup().add(commands_button).add(datasets_button).add(predictions_button)

COMMANDS_CAPTION = """🗒️ <b>Docs for available commands</b>

USER
• /start: Command for start

• /database: Command for database overview

• /predict: Command to predict prices.

ADMIN
• /scrape: Command for start scraper, scraper will scrape all websites links from https://cryptolinks.com

• /fetch_blocks: Command to fetch blocks data, sync all blocks from latest on db till latest on chain. 
        Use <code>'/fetch_blocks 101 159'</code> for custom range.

• /fetch_ticker: Command to fetch ticker data, sync all candles from latest on db till latest on exchange. 
        Use <code>'/fetch_ticker ETHUSDT'</code> for ETH and USDT ticker.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor tristique sagittis. 
"""
back_button = InlineKeyboardButton(text="⬅️ Back", callback_data="BACK_TO_START_BUTTON")
COMMANDS_KEYBOARD = InlineKeyboardMarkup().add(back_button)

# async def timer_func(message):
#     for i in range(1):
#        await message.answer(f"Starting scraping!{i}")
#        await asyncio.sleep(1) 
#     return True

async def start_command(message: types.Message):
    # await timer_func(message)
    with session:
        user_in_db = session.query(Users).filter(Users.tg_id == message.from_user.id).first()
        if not user_in_db:
            user = Users(message.from_user.first_name, message.from_user.username, message.from_user.id, message.chat.id, "user")
            session.add(user)
            session.commit()
    try:
        await bot.send_animation(chat_id=message.from_user.id, caption=START_CAPTION, animation=BANNER, reply_markup=START_KEYBOARD, parse_mode="HTML")
    except:
        await message.reply('Find me here! \n t.me/ai_course_test_bot')

async def comands_button_callback(callback: types.CallbackQuery):
        await callback.answer("Commands")
        await callback.message.edit_caption(COMMANDS_CAPTION, parse_mode="HTML")
        await callback.message.edit_reply_markup(COMMANDS_KEYBOARD)
    
async def back_button_callback(callback: types.CallbackQuery):
        await callback.message.edit_caption(START_CAPTION, parse_mode="HTML")
        await callback.message.edit_reply_markup(START_KEYBOARD)

async def predictions_button_callback(callback: types.CallbackQuery):
        await callback.answer("Predictions clicked! 🖱️")


def register_user_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])  
    dp.register_callback_query_handler(comands_button_callback, lambda query: query.data in ["COMMANDS_BUTTON"])  
    dp.register_callback_query_handler(back_button_callback, lambda query: query.data in ["BACK_TO_START_BUTTON"])  
    dp.register_callback_query_handler(predictions_button_callback, lambda query: query.data in ["PREDICTIONS_BUTTON"])  
    dp.register_callback_query_handler(start_command, lambda query: query.data in ["HOME_BUTTON"])  


