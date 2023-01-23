from aiogram.types import Message
from config import admin


def is_admin(message: Message) -> bool:
    if message.from_user.id == int(admin):
        return True
