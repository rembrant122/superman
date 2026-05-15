from enum import Enum

from aiogram import Bot, Dispatcher, F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bots.web_app_url import repeat_web_app_skill, memor_web_app_skill
from db.db_all import User
from db.db_basic import session_scope
from settings import TEXT_STARt_ENG_BOT, TOKEN_SKILLS

bot = Bot(TOKEN_SKILLS)
dp = Dispatcher()
router = Router()


class MainMenuEnums(Enum):
    START_REPEAT = "📱 НАЧАТЬ ПОВТОРЕНИЕ НАВЫКОВ"
    START_MEMORIZATION="🦣 НАЧАТЬ ИЗУЧЕНИЕ НОВЫХ НАВЫКОВ"
    STOP_NOTIF = "🔕 Не напоминать"
    START_NOTIF = "🔔 Напоминать"


def get_main_menu(user:User) -> ReplyKeyboardMarkup:

    notif_text = (
        MainMenuEnums.STOP_NOTIF.value
        if user.notify_for_skills_enabled
        else MainMenuEnums.START_NOTIF.value
    )

    return (ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MainMenuEnums.START_REPEAT.value, web_app=repeat_web_app_skill(user))],
            [KeyboardButton(text=MainMenuEnums.START_MEMORIZATION.value, web_app=memor_web_app_skill(user))],
            [KeyboardButton(text=notif_text)],
        ],
        resize_keyboard=True,
    )

@router.message(CommandStart()))
async def notif(notify_enabled:bool,message: Message):
    with session_scope() as session:
        user:User = User.find_by(session,tg_id=message.from_user.id).first()
        user.notify_for_skills_enabled = notify_enabled

    if notify_enabled: t = 'включены'
    else:t = 'выключены'

    await message.answer(
        f"🔔 Напоминания {t}",
        reply_markup=get_main_menu(user,),
    )

@router.message(F.text == MainMenuEnums.STOP_NOTIF.value)
async def handle_stop_notif(message: Message) -> None:
    await notif(notify_enabled=False, message=message)

@router.message(F.text == MainMenuEnums.START_NOTIF.value)
async def handle_start_notif(message: Message) -> None:
    await notif(notify_enabled=True, message=message)

@router.message(CommandStart())
async def start(message: Message) -> None:
    with session_scope() as session:
        tg_id = message.from_user.id

        user = User.find_by(session,tg_id=tg_id).first()

        if not user:
            user = User.add_something(session,tg_id=tg_id)

    photo_url = "https://drive.google.com/uc?export=view&id=1y8l8R8JrHxUh8mU9iRxhQ2V5mmyrB9Vc"

    reply_markup=get_main_menu(user)

    await message.answer_photo(
        photo=photo_url,
        caption=TEXT_STARt_ENG_BOT,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,# type: ignore
    )
