import asyncio
import aioschedule

async def send_message_1():
    print("Send first message")

async def send_message_2():
    print("Send second message")

async def scheduler():
    aioschedule.every().day.at("17:45").do(send_message_1)
    aioschedule.every().day.at("17:46").do(send_message_2)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)