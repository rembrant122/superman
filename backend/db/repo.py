from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import Session

from db.db_all import Skill, Dictionary, Word
from db.user import User


def register_user(session: Session,tg_id: int, tg_login: str) -> "User":
    user = User.find_by(session,tg_id=str(tg_id)).first()

    if user is None:
        user = User.add_something(session,
            tg_id=str(tg_id),
            tg_login=tg_login,
        )
    return user


def get_users_for_reminder_skills(session: Session) -> list[User]:
    l_us = (session.query(User).
            join(Skill, Skill.user_id == User.id).
            filter(Skill.next_date_time_for_repeat <= func.now(), Skill.stage > 0, ).all())
    return cast(list[User],l_us)


def get_users_with_ready_words_for_notify_skills(session:Session) -> list[User]:
    l_us=(((session.query(User).join(Dictionary, Dictionary.user_id == User.id)
          .join(Word, Word.dict_id == Dictionary.id)).filter(
            Dictionary.notify_enabled.is_(True),
            Dictionary.notify_already_sent.is_(False),
            Word.next_date_time_for_repeat <= func.now(),
            Word.stage > 0,
        )).distinct()).all()
    return cast(list[User],l_us)
