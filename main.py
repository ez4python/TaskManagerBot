import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold
from sqlalchemy import insert, select
from dotenv import load_dotenv
from reply import *
from db import User, session

load_dotenv()
# ADMIN_USER_ID = 1998050207
TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


# Statement Class
class UserStates(StatesGroup):
    main_menu = State()
    new_task = State()
    my_lists = State()


class TaskStates(StatesGroup):
    title = State()
    description = State()
    request_to_save = State()


@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    start = BotCommand(command='start', description='Start the bot')
    restart = BotCommand(command='restart', description='Restart the bot')
    await msg.bot.set_my_commands(commands=[start, restart])
    user_data = {
        'telegram_id': msg.from_user.id,
        'first_name': msg.from_user.first_name,
        'last_name': msg.from_user.last_name,
        'username': msg.from_user.username
    }
    user: User | None = session.execute(select(User).where(User.telegram_id == msg.from_user.id)).fetchone()
    if not user:
        query = insert(User).values(**user_data)
        session.execute(query)
        session.commit()
        await msg.answer('Welcome 🤗')
    else:
        user = user[0]
        if not user.last_name:
            if not user.first_name:
                await msg.answer('Welcome, user!')
            await msg.answer(f'Welcome, {user.first_name}!', reply_markup=main_menu_buttons())
        else:
            await msg.answer(f'Welcome, {user.first_name} {user.last_name}',
                             reply_markup=main_menu_buttons())
    await msg.answer(text="Choose menu 👇", reply_markup=main_menu_buttons())
    await state.set_state(UserStates.main_menu)


@dp.message(UserStates.main_menu)
async def main_menu_handler(msg: Message, state: FSMContext):
    if msg.text == "New 📝":
        await state.set_state(UserStates.new_task)
    elif msg.text == "My tasks 📋":
        await state.set_state(UserStates.my_lists)


@dp.message(UserStates.new_task)
async def new_task_handler(msg: Message, state: FSMContext):
    pass


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
