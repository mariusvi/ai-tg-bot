import asyncio
import aioschedule
from utils.fetcher.fetch_blocks import Fetch_blocks

fetcher = Fetch_blocks()

async def send_message_1():
    print("Send first message")

async def send_message_2():
    await asyncio.get_running_loop().run_in_executor(None, fetcher.start_fetch, 16203174,16203177, 1)  


async def scheduler():
    aioschedule.every().day.at("17:45").do(send_message_1)
    aioschedule.every().day.at("14:33").do(send_message_2)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)