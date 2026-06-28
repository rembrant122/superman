import asyncio
from enum import Enum

from aiogram import Bot, Dispatcher, F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from web_app_url import repeat_web_app, memor_web_app

from db.db_basic import session_scope
from superman.models.models_superman import parse_words_string

from db.db_all import Dictionary, add_words, CommonDictionary
from db.user import User
from db.repo import get_users_with_ready_words_for_notify_skills
from settings import TEXT_STARt_ENG_BOT, COMMON_DIC_ID, TOKEN_WORDS_ENG
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(TOKEN_WORDS_ENG)
dp = Dispatcher()
router = Router()

class MainMenuEnums(Enum):
    SAVE_WORDS = "💾 Загрузить в словарь"
    START_REPEAT = "📱 НАЧАТЬ ПОВТОРЕНИЕ"
    START_MEMORIZATION="🦣 НАЧАТЬ ЗАПОМИНАНИЕ НОВЫХ СЛОВ"
    STOP_NOTIF = "🔕 Не напоминать"
    START_NOTIF = "🔔 Напоминать"

class SaveWordsState(StatesGroup):
    waiting_words = State()

def get_main_menu(user:User,notify_enabled: bool = True) -> ReplyKeyboardMarkup:
    notif_text = (
        MainMenuEnums.STOP_NOTIF.value
        if notify_enabled
        else MainMenuEnums.START_NOTIF.value
    )

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MainMenuEnums.SAVE_WORDS.value)],
            [KeyboardButton(text=MainMenuEnums.START_REPEAT.value, web_app=repeat_web_app(user))],
            [KeyboardButton(text=MainMenuEnums.START_MEMORIZATION.value, web_app=memor_web_app(user))],
            [KeyboardButton(text=notif_text)],
        ],
        resize_keyboard=True,
    )

@router.message(CommandStart())
async def start(message: Message) -> None:
    """
    создать юзера если нет
    создать ему юзерский словарь для анг если нет
    """
    with session_scope() as session:

        tg_id = message.from_user.id

        user=User.find_by(session,tg_id=tg_id).first()

        if not user:
            user=User.add_something(session,tg_id=tg_id)

        dct:Dictionary=Dictionary.find_by(session,user_id=user.id, common_dictionary_id=COMMON_DIC_ID).first()
        if not dct:
            dct=Dictionary.add_something(session,user_id=user.id, common_dictionary_id=COMMON_DIC_ID,name='English words')

    photo_url = "https://drive.google.com/uc?export=view&id=1y8l8R8JrHxUh8mU9iRxhQ2V5mmyrB9Vc"

    await message.answer_photo(
        photo=photo_url,
        caption=TEXT_STARt_ENG_BOT,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu(user,dct.notify_enabled),
    )

#напоминалка
async def remind_notif():
    with session_scope() as session:

        users:list[User]=get_users_with_ready_words_for_notify_skills(session)

        for u in users:
            dct:Dictionary=Dictionary.find_by(session,user_id=u.id, common_dictionary_id=COMMON_DIC_ID).first()
            dct.notify_already_sent=True


    for user in users:
        try:
            keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔁 Повторить!", web_app=repeat_web_app(user))]],
                                           resize_keyboard=True)

            await bot.send_message(
                chat_id=user.tg_id,
                text="⏰ Пора повторить слова!",
                reply_markup=keyboard
            )

            await asyncio.sleep(0.05)  # защита от флуда

        except TelegramForbiddenError:

            # бот заблокирован
            continue
        except TelegramBadRequest:
            # кривой chat_id или др ошибка запроса
            continue

@router.message(F.text == MainMenuEnums.SAVE_WORDS.value)
async def handle_save_words(message: Message, state: FSMContext):
    """

    id: int
    word: str
    translate: str
    transcription: str | None = None
    context:str| None = None

    """

    await state.set_state(SaveWordsState.waiting_words)
    await message.answer("Пришли слова:"
                         "\nword|перевод|transcription|context")

@router.message(SaveWordsState.waiting_words)
async def handle_words_for_save(message: Message, state: FSMContext):

    words=parse_words_string(message.text)
    if words is False:
        await message.answer("ФОРМАТ НЕ ВЕРЕН! НАЖМИ ПОСТОРНО ЗАГРУЗИТЬ СЛОВАРЬ И ВВЕДИ В ПРАВИЛЬНОМ ФОРМАТЕ")
    else:
        with session_scope() as session:
            c_d=CommonDictionary.find_by_id(session,COMMON_DIC_ID)
            user=User.find_by(session,tg_id=message.from_user.id).first()
            add_words(session,c_d,user,words)

        await state.clear()
        await message.answer('СЛОВА СОХРАНЕНЫ!')


async def notif(notify_enabled:bool,message: Message):

    with session_scope() as session:
        user = User.find_by(session,tg_id=message.from_user.id).first()

        dct: Dictionary | None = Dictionary.find_by(session,
            user_id=user.id,
            common_dictionary_id=COMMON_DIC_ID,
        ).first()
        dct.notify_enabled = notify_enabled

    if notify_enabled: t = 'включены'
    else:t = 'выключены'

    await message.answer(
        f"🔔 Напоминания {t}",
        reply_markup=get_main_menu(user,notify_enabled),
    )

@router.message(F.text == MainMenuEnums.STOP_NOTIF.value)
async def handle_stop_notif(message: Message) -> None:
    await notif(notify_enabled=False, message=message)


@router.message(F.text == MainMenuEnums.START_NOTIF.value)
async def handle_start_notif(message: Message) -> None:
    await notif(notify_enabled=True, message=message)

dp.include_router(router)

async def run_bot() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
