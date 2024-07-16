from aiogram.filters import BaseFilter
from aiogram.types import Message, ContentType


class SupportedFilter(BaseFilter):
    """Filters out anything that isn't document, photo or video"""

    async def __call__(self, message: Message) -> bool:
        return message.content_type in (
            ContentType.DOCUMENT,
            ContentType.PHOTO,
            ContentType.VIDEO,
        )
