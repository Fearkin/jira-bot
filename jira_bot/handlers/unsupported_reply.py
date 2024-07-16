from aiogram import Router, F
from aiogram.types import Message

from jira_bot.config.settings import config

router = Router()


@router.message(F.reply_to_message, F.chat.id == config.admin_chat_id, F.poll)
async def unsupported_admin_reply_types(message: Message):
    """Warns either side that it's impossible to send poll"""
    await message.reply("Polls not supported")
