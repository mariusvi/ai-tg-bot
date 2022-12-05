from aiogram import executor
from bot import dp


async def on_startup(_):
    print("Bot started!")

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


