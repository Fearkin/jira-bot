from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_commands(bot: Bot):
    """Sets up bot's commands"""
    usercommands = [
        BotCommand(command="help", description="Show help message"),
        BotCommand(command="new", description="Create issue"),
        BotCommand(command="stop", description="Cancel current action"),
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())
