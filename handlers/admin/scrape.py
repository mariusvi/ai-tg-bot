from aiogram import types, Dispatcher
from web_scraper.scraper import Scraper
from database.db import get_session
from database.models.Data_sources import Data_sources
from datetime import datetime
import asyncio
from utils.helpers.helpers import is_admin

scraper = Scraper()
session = get_session()


async def scrape_command(message: types.Message):
    if is_admin(message):
        before = datetime.now()
        await message.answer("Start scraping!")
        data = await asyncio.get_running_loop().run_in_executor(
            None, scraper.scrape, "", ["crypto"]
        )
        with session:
            for scraper_data in data:
                for item in scraper_data["items"]:
                    if (
                        not session.query(Data_sources)
                        .filter(Data_sources.name == item.title)
                        .first()
                    ):
                        payload = Data_sources(
                            name=item.title,
                            category=item.category,
                            url=item.url,
                            description=item.description,
                            icon=item.icon,
                        )
                        session.add(payload)
                        session.commit()
        result = datetime.now() - before
        await message.answer(f"Job finished! Total time: {result}")
    else:
        await message.answer("Only admin can use this command!")


def register_admin_scrape_handlers(dp: Dispatcher):
    dp.register_message_handler(scrape_command, commands=["scrape"])
