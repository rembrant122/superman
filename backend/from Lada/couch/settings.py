import pymysql

# ----- НАСТРОЙКИ БОТА / ПРИЛОЖЕНИЯ / БД -----

BOT_TOKEN = "8099342604:AAG89kOiECBlrjhGluKPbiAdbhR0S8cq0rs"
#URL_WEB_APP = "https://preallied-karter-moaningly.ngrok-free.dev/"
TG_LOGIN_ADMIN = "Shokolada108"

# ----- БАЗА ДАННЫХ  -----

#DB_PATH = "polyglot.db"
DB_CONFIG = {
    "host": "Shokolad.mysql.pythonanywhere-services.com",
    "user": "ShokoLad",
    "password": "Efepolat1",
    "database": "ShokoLad$skills",
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
