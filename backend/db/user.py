import secrets
from typing import TYPE_CHECKING, cast

from sqlalchemy import String, and_, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from db.db_basic import AutomatisationDataBase
from db.zoar_user import UserZoar

if TYPE_CHECKING:
    from db.db_all import Skill, Dictionary, Word


def generate_token() -> str:
    return secrets.token_hex(16)


class UserSuperman(AutomatisationDataBase):
    __abstract__ = True

    notify_for_skills_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_for_skills_already_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # после того как отправили - ставит True, после повторения - снова False
    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    ready_skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        primaryjoin=lambda: and_(
            User.id == Skill.user_id,
            Skill.next_date_time_for_repeat <= func.now(),
            Skill.stage > 0,
        ),
        viewonly=True,
        lazy="select",
    )

    ...


class User(UserSuperman,UserZoar):
    __tablename__ = "users"

    tg_id: Mapped[str] = mapped_column(String, unique=True)
    tg_login: Mapped[str] = mapped_column(String, default="")


    token: Mapped[str] = mapped_column(String, default=generate_token)


def register_user(session: Session,tg_id: int, tg_login: str) -> "User":
    user = User.find_by(session,tg_id=str(tg_id)).first()

    if user is None:
        user = User.add_something(session,
            tg_id=str(tg_id),
            tg_login=tg_login,
        )
    return user


def get_users_for_reminder(session: Session) -> list[User]:
    l_us = (session.query(User).
            join(Skill, Skill.user_id == User.id).
            filter(Skill.next_date_time_for_repeat <= func.now(), Skill.stage > 0, ).all())
    return cast(list[User],l_us)


def get_users_with_ready_words_for_notify(session:Session) -> list[User]:
    l_us=(((session.query(User).join(Dictionary, Dictionary.user_id == User.id)
          .join(Word, Word.dict_id == Dictionary.id)).filter(
            Dictionary.notify_enabled.is_(True),
            Dictionary.notify_already_sent.is_(False),
            Word.next_date_time_for_repeat <= func.now(),
            Word.stage > 0,
        )).distinct()).all()
    return cast(list[User],l_us)
