import secrets
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_basic import AutomatisationDataBase

if TYPE_CHECKING:
    from db.db_all import Skill

def generate_token() -> str:
    return secrets.token_hex(16)

#
# class UserSuperman(AutomatisationDataBase):
#     __abstract__ = True
#
#
#     ...


class User(AutomatisationDataBase
    # UserSuperman,
           # UserZoar
           ):
    __tablename__ = "users"

    tg_id: Mapped[str] = mapped_column(String, unique=True)
    tg_login: Mapped[str] = mapped_column(String, default="")

    token: Mapped[str] = mapped_column(String, default=generate_token)

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
    #
    # ready_skills: Mapped[list["Skill"]] = relationship(
    #     "Skill",
    #     primaryjoin=lambda: and_(
    #         User.id == Skill.user_id,
    #         Skill.next_date_time_for_repeat <= func.now(),
    #         Skill.stage > 0,
    #     ),
    #     viewonly=True,
    #     lazy="select",
    # )
