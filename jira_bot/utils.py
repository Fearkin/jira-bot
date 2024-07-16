from collections.abc import Sequence
from dataclasses import dataclass
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


@dataclass
class Ticket:
    """Represents ticket"""

    project: str
    username: str
    problem_type: str
    problem_name: str
    problem_desc: str


def get_keyboard(items: Sequence[int | str], size: int = 1) -> ReplyKeyboardMarkup:
    """Creates keyboard from provided sequence and size"""
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.button(text=item)
    builder.adjust(size)
    return builder.as_markup(resize_keyboard=True)
