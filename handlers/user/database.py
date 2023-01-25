from aiogram import types, Dispatcher
from src.bot import dp, bot
from sqlalchemy import desc
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import get_session
from database.models.Block import Block
from database.models.Data_sources import Data_sources
from database.models.Tx import Tx
from database.models.Receipt import Receipt
from database.models.Ticker_ETHUSDT_15m import Ticker_ETHUSDT_15m
from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as fplt
import pandas as pd
import base64
import io


session = get_session()

BANNER = "https://cdn.dribbble.com/users/1373613/screenshots/5385718/media/30cede328265c92d61aa211591e70b62.gif"

blocks_button = InlineKeyboardButton(text="Blocks", callback_data="BLOCKS_BUTTON")
ticker_button = InlineKeyboardButton(text="Ticker", callback_data="TICKER_BUTTON")
news_button = InlineKeyboardButton(text="News", callback_data="NEWS_BUTTON")
home_button = InlineKeyboardButton(text="Home", callback_data="HOME_BUTTON")
DATABASE_KEYBOARD = (
    InlineKeyboardMarkup().add(blocks_button).add(ticker_button).add(news_button).add(home_button)
)

back_button = InlineKeyboardButton(text="⬅️ Back", callback_data="BACK_TO_DATABASE_BUTTON")
BLOCKS_KEYBOARD = InlineKeyboardMarkup().add(back_button)


async def database_command(message: types.Message):
    with session:
        all_blocks = session.query(Block).all()
        data_sources = session.query(Data_sources).all()
        ticker = session.query(Ticker_ETHUSDT_15m).all()
    m = """<b>Database</b>

    Links in database: {}
    
    Blocks in database: {}

    News in database: 0

    Candles in ticker: {}
    
    """.format(
        len(data_sources), len(all_blocks), len(ticker)
    )
    await bot.send_animation(
        message.from_user.id,
        caption=m,
        animation=BANNER,
        reply_markup=DATABASE_KEYBOARD,
        parse_mode="HTML",
    )


async def blocks_button_callback(callback: types.CallbackQuery):
    await callback.message.edit_caption(
        caption="loading...", reply_markup=BLOCKS_KEYBOARD, parse_mode="HTML"
    )
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
        
    """.format(
        len(all_blocks), len(all_tx), len(all_receipt), last_block_in_db, last_block_timestamp
    )
    await callback.message.edit_caption(caption=m, reply_markup=BLOCKS_KEYBOARD, parse_mode="HTML")


async def ticker_button_callback(callback: types.CallbackQuery):
    with session:
        ticker = session.query(Ticker_ETHUSDT_15m).all()
    total = len(ticker)
    ticker_df = pd.DataFrame([row.__dict__ for row in ticker]).tail(50)

    ticker = ticker_df.loc[
        :,
        ("open_time", "close_time", "open", "close", "high", "low", "volume", "number_of_trades"),
    ]
    ticker["open_date"] = ticker["open_time"].values.astype(dtype="datetime64[ms]")
    ticker["close_date"] = ticker["close_time"].values.astype(dtype="datetime64[ms]")
    ticker.index = pd.DatetimeIndex(ticker["open_date"])
    fig, axs = plt.subplots(3, sharex=True, figsize=(12, 10))
    fig.suptitle("Data from Binance ticker (last 50 candles)")
    axs[0].plot(ticker["open_date"], ticker["close"], color="green", label="ETH price", lw=2)
    axs[0].set_title("ETH price")
    axs[0].set_ylabel("price (USD)")
    axs[1].plot(ticker["open_date"], ticker["volume"], color="blue", label="volume", lw=2)
    axs[1].set_title("Trades volume")
    axs[1].set_ylabel("ETH")
    axs[2].plot(
        ticker["open_date"],
        ticker["number_of_trades"],
        color="magenta",
        label="trades count",
        lw=2,
    )
    axs[2].set_title("Trades count")
    axs[2].set_ylabel("trades")
    fig.legend()
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
    )
    buf.seek(0)

    m = """<b>Ticker</b>

        Total candles in ticker: {}
        
        <b>Last candle</b>

        Open time: {} 

        Close time: {}
        
        Open price: {} USD

        Close price: {} USD
        
        """.format(
        total,
        pd.to_datetime(ticker["open_date"].tail(1).values[0]),
        pd.to_datetime(ticker["close_date"].tail(1).values[0]),
        ticker["open"].tail(1).values[0],
        ticker["close"].tail(1).values[0],
    )
    await callback.message.answer_photo(buf)
    await callback.message.edit_caption(caption=m, reply_markup=BLOCKS_KEYBOARD, parse_mode="HTML")



async def news_button_callback(callback: types.CallbackQuery):
    await callback.message.edit_caption("Empty", reply_markup=DATABASE_KEYBOARD)



def register_user_database_handlers(dp: Dispatcher):
    dp.register_message_handler(database_command, commands=["database"])
    dp.register_callback_query_handler(
        blocks_button_callback, lambda query: query.data in ["BLOCKS_BUTTON"]
    )
    dp.register_callback_query_handler(
        ticker_button_callback, lambda query: query.data in ["TICKER_BUTTON"]
    )
    dp.register_callback_query_handler(
        news_button_callback, lambda query: query.data in ["NEWS_BUTTON"]
    )
    dp.register_callback_query_handler(
        database_command, lambda query: query.data in ["BACK_TO_DATABASE_BUTTON"]
    )
    dp.register_callback_query_handler(
        database_command, lambda query: query.data in ["DATABASE_BUTTON"]
    )
