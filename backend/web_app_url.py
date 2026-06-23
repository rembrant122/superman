from aiogram.types import WebAppInfo

from db.user import User
from settings import URL_WEB_APP


def _build_web_app(user: User, app: str, repeat: bool) -> WebAppInfo:
    url = f"{URL_WEB_APP}?app={app}&repeat={str(repeat).lower()}&token={user.token}"
    return WebAppInfo(url=url)


def repeat_web_app(user: User) -> WebAppInfo:
    return _build_web_app(user, app="eng_words", repeat=True)


def memor_web_app(user: User) -> WebAppInfo:
    return _build_web_app(user, app="eng_words", repeat=False)

def repeat_web_app_skill(user: User) -> WebAppInfo:
    return _build_web_app(user, app="skills", repeat=True)


def memor_web_app_skill(user: User) -> WebAppInfo:
    return _build_web_app(user, app="skills", repeat=False)
