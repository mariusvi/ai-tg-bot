import asyncio
import aioschedule
from utils.fetcher.fetch_blocks import Fetch_blocks

fetcher = Fetch_blocks()


async def send_message_1():
    print("Send first message")


async def send_message_2():
    print("Send second message")


async def update_db():
    await asyncio.get_running_loop().run_in_executor(None, fetcher.start_fetch)


async def scheduler():
    aioschedule.every().day.at("00:00").do(update_db)
    aioschedule.every().day.at("17:45").do(send_message_1)
    aioschedule.every().day.at("14:33").do(send_message_2)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
