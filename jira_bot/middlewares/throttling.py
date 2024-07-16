from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """Throttles messages with given timer and shows warning"""

    def __init__(self, throttle_time: int):
        self.caches = {
            "user": TTLCache(maxsize=10_000, ttl=throttle_time),
            "base": TTLCache(maxsize=10_000, ttl=throttle_time),
        }

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                await event.answer(
                    "Only one message per 30 second period is allowed",
                    show_alert=True,
                )
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
