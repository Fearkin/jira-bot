from asyncio import create_task, sleep

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import ContentType, Message


from jira_bot.filters.supportedtypes import SupportedFilter
from jira_bot.config.settings import config

router = Router()
base_flags = {"throttling_key": "base"}
user_flags = {"throttling_key": "user"}


async def _send_expiring_notification(message: Message):
    """Notifies user about sended message and deletes itself"""
    msg = await message.reply("Message sent")
    await sleep(5.0)
    await msg.delete()


@router.message(Command(commands=["help"]), flags=base_flags)
async def cmd_help(message: Message):
    """Shows help"""
    await message.answer(
        "Use /new \n\n to create issue. You can also send messages directly using this chat. Sending text messages, videos and photos is allowed"
    )


@router.message(Command(commands=["start"]), flags=base_flags)
async def cmd_start(message: Message):
    """Starts bot"""
    await message.answer(
        "Use /new \n\n to create issue. You can also send messages directly using this chat. Sending text messages, videos and photos is allowed"
    )


@router.message(F.text & ~F.text.startswith("/"), flags=user_flags)
async def text_message(message: Message, bot: Bot):
    """Sends text message to admin_chat"""
    if len(message.text) > 200:
        return await message.reply("Symbol limit reached (200)")
    else:
        await bot.send_message(
            config.admin_chat_id,
            message.html_text
            + f"\n\n@{message.from_user.username}\n\n#id{message.from_user.id}",
            parse_mode="HTML",
        )
        create_task(_send_expiring_notification(message))


@router.message(SupportedFilter())
async def supported_media(message: Message):
    """Sends media to admin_chat"""
    if message.caption and len(message.caption) > 200:
        return await message.reply("Symbol limit reached (200)")
    else:
        await message.copy_to(
            config.admin_chat_id,
            caption=(
                (message.caption or "")
                + f"\n\n@{message.from_user.username}\n\n#id{message.from_user.id}"
            ),
            parse_mode="HTML",
        )
        create_task(_send_expiring_notification(message))


@router.message()
async def unsupported_types(message: Message):
    """Warns about incorrect message type"""
    if message.content_type not in (
        ContentType.NEW_CHAT_MEMBERS,
        ContentType.LEFT_CHAT_MEMBER,
        ContentType.VIDEO_CHAT_STARTED,
        ContentType.VIDEO_CHAT_ENDED,
        ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED,
        ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED,
        ContentType.NEW_CHAT_PHOTO,
        ContentType.DELETE_CHAT_PHOTO,
        ContentType.SUCCESSFUL_PAYMENT,
        "proximity_alert_triggered",
        ContentType.NEW_CHAT_TITLE,
        ContentType.PINNED_MESSAGE,
    ):
        await message.reply("Message type not supported")
