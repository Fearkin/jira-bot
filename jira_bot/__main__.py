"""Entrypoint of the program"""

import asyncio
import structlog
import sys
import logging

from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from jira_bot.commands import set_bot_commands
from jira_bot.handlers import setup_routers
from dishka.integrations.aiogram import setup_dishka

from jira_bot.config.settings import config
from jira_bot.middlewares.throttling import ThrottlingMiddleware
from jira_bot.config.ioc import container


async def main() -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    log = structlog.stdlib.get_logger(__name__)
    dp = Dispatcher(storage=RedisStorage.from_url(str(config.redis)), config=config)
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties())

    router = setup_routers()
    dp.include_router(router)
    dp.message.middleware(ThrottlingMiddleware(throttle_time=20))

    setup_dishka(container=container, router=dp, auto_inject=True)
    await set_bot_commands(bot)
    try:
        await bot.delete_webhook()
        await log.ainfo("starting...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await log.ainfo("closing...")
        await container.close()
        await bot.session.close()


asyncio.run(main())
