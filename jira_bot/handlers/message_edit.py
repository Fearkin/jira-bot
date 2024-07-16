from aiogram import Router
from aiogram.types import Message


router = Router()


@router.edited_message()
async def edited_message_warning(message: Message):
    """Warns either side that it's impossible to edit message"""
    await message.reply("Message cannot be edited")
