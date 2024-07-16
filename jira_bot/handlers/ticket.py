import asyncio
from aiogram import F, Bot, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka
from jira import JIRA
from aiogram.filters import Command
import structlog
from jira_bot.jira_manager import create_ticket
from jira_bot.utils import Ticket, get_keyboard
from functools import partial
from jira_bot.config.settings import config

router = Router()
log = structlog.stdlib.get_logger(__name__)


class TicketForm(StatesGroup):
    """State-class to control dialog flow"""

    project = State()
    problem_type = State()
    problem_name = State()
    problem_desc = State()
    send_ticket = State()


available_projects = config.projects
available_problem_types = config.problem_types


@router.message(Command(commands=["new"]))
async def get_project(message: Message, state: FSMContext):
    """Start new dialog"""
    await message.answer(
        "Choose project", reply_markup=get_keyboard(available_projects, 2)
    )
    await state.set_state(TicketForm.project)


@router.message(Command(commands=["stop"]))
async def cmd_stop(message: Message, state: FSMContext):
    """Stops dialog if present and resets state"""
    await state.clear()
    await message.answer(text="Action is canceled", reply_markup=ReplyKeyboardRemove())


@router.message(TicketForm.project, F.text.in_(available_projects))
async def get_problem_type(message: Message, state: FSMContext):
    """Gets problem type from user and sets new state if correct project is chosen"""
    await state.update_data(project=message.text)
    await message.answer(
        "Choose problem type", reply_markup=get_keyboard(available_problem_types, 2)
    )
    await state.set_state(TicketForm.problem_type)


@router.message(TicketForm.project)
async def incorrect_project(message: Message):
    """Returns error message but doesn't change the state"""
    await message.answer(
        "Incorrect project", reply_markup=get_keyboard(available_projects, 2)
    )


@router.message(TicketForm.problem_type, F.text.in_(available_problem_types))
async def get_problem_name(message: Message, state: FSMContext):
    """Gets problem name from user and sets new state if correct problem type is chosen"""
    await message.answer("Problem name:", reply_markup=ReplyKeyboardRemove())
    await state.update_data(problem_type=message.text)
    await state.set_state(TicketForm.problem_name)


@router.message(TicketForm.problem_type)
async def incorrect_problem_type(message: Message):
    """Returns error message but doesn't change the state"""
    await message.answer(
        "Incorrect problem type", reply_markup=get_keyboard(available_problem_types)
    )


@router.message(TicketForm.problem_name, (10 <= F.text.len()) & (F.text.len() < 200))
async def get_problem_desc(message: Message, state: FSMContext):
    """Gets problem description from user and sets new state if ticket name is correct"""
    await state.update_data(problem_name=message.text)
    await message.answer("Describe your problem", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TicketForm.problem_desc)


@router.message(TicketForm.problem_name)
async def incorrect_problem_name(message: Message):
    """Returns error message but doesn't change the state"""
    if len(message.text) > 200:
        await message.answer("Symbol limit reached (200)")
    if len(message.text) < 10:
        await message.answer("Minimal symbol count - 10")


@router.message(TicketForm.problem_desc, (10 <= F.text.len()) & (F.text.len() < 200))
async def get_phone_number(message: Message, state: FSMContext):
    """Gets phone number from user and sets new state if ticket description is correct"""
    await state.update_data(problem_desc=message.text)
    await message.answer(
        "Provide phone number if you want to",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(TicketForm.send_ticket)


@router.message(TicketForm.problem_desc)
async def incorrect_description(message: Message):
    """Returns error message but doesn't change the state"""
    if len(message.text) > 1000:
        await message.answer("Symbol limit reached (1000)")
    if len(message.text) < 10:
        await message.answer("Minimal symbol count - 10")


@router.message(TicketForm.send_ticket)
async def send_ticket(
    message: Message, bot: Bot, state: FSMContext, jira: FromDishka[JIRA]
):
    """Creates new ticket using user-provided data"""
    await state.update_data(username=message.text)
    data = await state.get_data()
    data = Ticket(**data)
    loop = asyncio.get_running_loop()
    issue_fields = await loop.run_in_executor(
        None, partial(create_ticket, data, jira)
    )  # create_ticket is a synchronious function and should be run apart from async code
    issue_message = (
        f"Issue key: {issue_fields['key']}\n\n"
        f"Name: {issue_fields['summary']}\n"
        f"Description: {issue_fields['description']}\n"
        f"Contact information: {issue_fields['customfield_10032']}\n"
        f"Problem type: {issue_fields['customfield_10033']}\n"
        f"Project: {issue_fields['customfield_10034']}\n\n"
        f"Username: @{message.from_user.username}\n"
        f"#id{message.from_user.id}\n"
    )
    await message.answer(
        "Issue created. You can send messages to Support Team through this chat.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot.send_message(config.admin_chat_id, issue_message, parse_mode="HTML")
    await state.clear()
