from pathlib import Path

from apiflask import APIFlask
from flask import request, send_from_directory

from app_flask.skills_app import skills_blueprint
from app_flask.words_app import words_blueprint

# ==========================================
# Базовая папка проекта.
# __file__ -> backend/app_flask/app_run.py
# parents[2] -> корень проекта superman
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[2]

# ==========================================
# Папка собранного фронта.
# Сюда vite кладет index.html и assets
# после команды npm run build
# ==========================================
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"

# ==========================================
# Папка с ассетами сборки фронта.
# Обычно vite кладет сюда js/css.
# ==========================================
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"


def log_request() -> None:
    """
    Лог входящего запроса.
    Удобно для отладки фронта и API.
    """
    print("\n➡️ REQUEST")
    print("URL:", request.url)
    print("METHOD:", request.method)
    print("HEADERS:", dict(request.headers))
    print("BODY:", request.get_data())


def log_response(response):
    """
    Лог исходящего ответа.
    """
    print("⬅️ RESPONSE")
    print("STATUS:", response.status)

    if response.direct_passthrough:
        print("BODY: <direct_passthrough>")
        return response

    try:
        print("BODY:", response.get_data(as_text=True))
    except Exception as error:
        print("BODY: <cannot read body>", error)

    return response


def create_app() -> APIFlask:
    """
    Создание Flask/APIFLask приложения.

    Что делает:
    1. включает логирование запросов/ответов
    2. настраивает BearerAuth для swagger
    3. регистрирует blueprints API
    4. отдает собранный Vue фронт из dist
    """
    app = APIFlask(__name__)

    app.before_request(log_request)
    app.after_request(log_response)

    app.config["SECURITY_SCHEMES"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    app.config["SECURITY"] = [{"BearerAuth": []}]

    app.register_blueprint(words_blueprint)
    app.register_blueprint(skills_blueprint)

    @app.get("/")
    def index():
        """
        Главная страница фронта.

        Возвращаем именно dist/index.html,
        а не исходный frontend/src/index.html.
        """
        return send_from_directory(FRONTEND_DIST_DIR, "index.html")

    @app.get("/assets/<path:filename>")
    def assets(filename: str):
        """
        Раздача js/css/прочих файлов сборки Vite.
        Например:
        /assets/index-xxxxx.js
        /assets/index-xxxxx.css
        """
        return send_from_directory(FRONTEND_ASSETS_DIR, filename)

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8000, debug=True)
