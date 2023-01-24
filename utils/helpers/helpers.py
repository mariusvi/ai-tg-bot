from aiogram.types import Message
from src.config import admin


def is_admin(message: Message) -> bool:
    if admin is not None:
        admin_id = int(admin)
    if message.from_user.id == admin_id:
        return True
    return False
