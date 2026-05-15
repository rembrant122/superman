import pymysql

# ----- ТОКЕН БОТА / АДРЕС ПРИЛОЖЕНИЯ -----

BOT_TOKEN = "8103834496:AAEikV6qS7fN8ZxV1Z66YsYBhSlrq68leA8"
TG_LOGIN_ADMIN = "DigitalGeisha108"

URL_WEB_APP = "https://polyglot-shokolad.pythonanywhere.com/"


# ----- БАЗА ДАННЫХ  -----

#DB_PATH = "polyglot.db"
DB_CONFIG = {
    "host": "Shokolad.mysql.pythonanywhere-services.com",
    "user": "ShokoLad",
    "password": "Efepolat1",
    "database": "ShokoLad$polyglot",
    "cursorclass": pymysql.cursors.DictCursor,
}


# ----- КЛЮЧ API  -----

OPENAI_API_KEY = "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"
OPENAI_MODEL = "gpt-4o-mini"


# ----- ПЕРЕМЕННЫЕ БОТА  -----

INTERVALS = [
    (1, 15),
    (2, 60),
    (3, 60 * 24),
    (4, 60 * 24 * 3),
    (5, 60 * 24 * 7),
    (6, 60 * 24 * 21),
]

COUNT_WORDS = 7

