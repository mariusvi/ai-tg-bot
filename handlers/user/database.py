from aiogram import types, Dispatcher
from bot import dp, bot
from sqlalchemy import desc
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import get_session
from database.models.Block import Block
from database.models.Data_sources import Data_sources
from database.models.Tx import Tx
from database.models.Receipt import Receipt
from datetime import datetime


session = get_session()

BANNER = "https://cdn.dribbble.com/users/1373613/screenshots/5385718/media/30cede328265c92d61aa211591e70b62.gif"

blocks_button = InlineKeyboardButton(text="Blocks", callback_data="BLOCKS_BUTTON")
ticker_button = InlineKeyboardButton(text="Ticker", callback_data="TICKER_BUTTON")
news_button = InlineKeyboardButton(text="News", callback_data="NEWS_BUTTON")
home_button = InlineKeyboardButton(text="Home", callback_data="HOME_BUTTON")
DATABASE_KEYBOARD = InlineKeyboardMarkup().add(blocks_button).add(ticker_button).add(news_button).add(home_button)

back_button = InlineKeyboardButton(text="⬅️ Back", callback_data="BACK_TO_DATABASE_BUTTON")
BLOCKS_KEYBOARD = InlineKeyboardMarkup().add(back_button)


async def database_command(message: types.Message):
    with session:
        all_blocks = session.query(Block).all()
        data_sources = session.query(Data_sources).all()
    m = """<b>Database</b>

    Links in database: {}
    
    Blocks in database: {}

    News in database: 0

    Tickers available:
        no tickers
    
    """.format(len(data_sources), len(all_blocks))
    await bot.send_animation(message.from_user.id, caption=m, animation=BANNER, reply_markup=DATABASE_KEYBOARD, parse_mode="HTML")

async def blocks_button_callback(callback: types.CallbackQuery):
    with session:
            all_blocks = session.query(Block.blockNumber).all()
            all_tx = session.query(Tx.tx_hash).all()
            all_receipt = session.query(Receipt.tx_hash).all()
            last_block_in_db_call = session.query(Block).order_by(desc(Block.blockNumber)).first()
            last_block_in_db = last_block_in_db_call.blockNumber
            last_block_timestamp = datetime.fromtimestamp(last_block_in_db_call.timestamp)
    m = """<b>Blocks</b>

    Blocks in database: {}
        
    Txs in database: {}

    Receipts in database: {}

    Last block: {}
    Block timestamp: {}
        
    """.format(len(all_blocks), len(all_tx), len(all_receipt), last_block_in_db, last_block_timestamp)
    await callback.message.edit_caption(caption=m, reply_markup=BLOCKS_KEYBOARD, parse_mode="HTML")
    # await callback.message.edit_caption("Commands", reply_markup=DATABASE_KEYBOARD)
        # await callback.message.edit_caption(COMMANDS_CAPTION, parse_mode="HTML")

async def ticker_button_callback(callback: types.CallbackQuery):
        await callback.message.edit_caption("Soon!", reply_markup=DATABASE_KEYBOARD)
        # await callback.message.edit_caption(COMMANDS_CAPTION, parse_mode="HTML")

async def news_button_callback(callback: types.CallbackQuery):
        await callback.message.edit_caption("Soon!", reply_markup=DATABASE_KEYBOARD)
        # await callback.message.edit_caption(COMMANDS_CAPTION, parse_mode="HTML")

def register_user_database_handlers(dp: Dispatcher):
    dp.register_message_handler(database_command, commands=['database'])
    dp.register_callback_query_handler(blocks_button_callback, lambda query: query.data in ["BLOCKS_BUTTON"])  
    dp.register_callback_query_handler(ticker_button_callback, lambda query: query.data in ["TICKER_BUTTON"])  
    dp.register_callback_query_handler(news_button_callback, lambda query: query.data in ["NEWS_BUTTON"])  
    dp.register_callback_query_handler(database_command, lambda query: query.data in ["BACK_TO_DATABASE_BUTTON"])  
    dp.register_callback_query_handler(database_command, lambda query: query.data in ["DATABASE_BUTTON"])  



