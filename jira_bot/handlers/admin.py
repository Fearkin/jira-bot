from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

from jira_bot.config.settings import config

router = Router()
router.message.filter(F.chat.id == config.admin_chat_id)


def extract_id(message: Message) -> int:
    """Extracts ID from last string of message"""
    entities = message.entities or message.caption_entities
    if not entities or entities[-1].type != "hashtag":
        raise ValueError("Can't extract ID from reply!")
    hashtag = entities[-1].extract_from(message.text or message.caption)
    if len(hashtag) < 4 or not hashtag[3:].isdigit():
        raise ValueError("Incorrect reply ID!")

    return int(hashtag[3:])


@router.message(F.reply_to_message)
async def reply_to_user(message: Message):
    """Sends reply to user"""
    try:
        user_id = extract_id(message.reply_to_message)
        print(user_id)
    except ValueError as ex:
        return await message.reply(str(ex))
    try:
        await message.copy_to(user_id)
    except TelegramAPIError:
        await message.reply("Unable to reply to user!")
