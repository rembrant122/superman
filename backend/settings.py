from pathlib import Path

COMMON_DIC_ID=0 #номер словаря, когда будут больше ботов будут другие ид
QUANTITY_WORDS_FOR_MEMORIZE=5

TEXT_STARt_ENG_BOT=(
        f"🎉 Привет!\n\n"
        "Я помогу тебе запомнить <b>много новых слов за короткое время!</b> 🧠 \n\n"
        "Мы будем использовать КРИВУЮ ЗАБЫВАНИЯ 📅 — и повторять слова только в нужное время!\n\n"
        "<i>Создавай словари, добавляй слова — я напомню, когда их нужно повторить.</i>\n"
        "<i>Если забудешь слово — его цикл начнётся заново.</i>\n\n"
        "В следующей версии:\n"
        "Ты сможешь послушать произношение слова, если забыл, как оно звучит!\n"
        "Я буду показывать тебе для слова маленькую картинку — чтобы запомнить было легче!\n"
    )
URL_WEB_APP = "https://k3fj2l.ngrok-free.app"
TOKEN_WORDS_ENG= '8611555695:AAH6aYfnwX9AfZD3v4FiA7k8aAWV3A4H380'#superman_learn_eng_bot
TOKEN_SKILLS='8771434024:AAFVl4JqQzERdrGOmYlATkwZyyjufkd9Ba4'#superman_couch_bot superman_couch
HOST="0.0.0.0"
PORT=8000
BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'superman.db'}"
