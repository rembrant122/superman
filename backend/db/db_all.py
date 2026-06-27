from datetime import datetime, UTC
from typing import cast

from sqlalchemy import Boolean, DateTime, ForeignKey, String, and_, func, or_
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
)
from sqlalchemy.orm import relationship

from enums import SkillType
from db.db_basic import AutomatisationDataBase, engine
from db.user import User
from superman.models.models_superman import WordModel
from superman.superman_controller.steps import get_next_step_time


def now_utc() -> datetime:
    return datetime.now(UTC)


class Word(AutomatisationDataBase):
    __tablename__ = "words"

    dict_id: Mapped[int] = mapped_column(Integer, ForeignKey("dictionaries.id"))
    dictionary: Mapped["Dictionary"] = relationship("Dictionary", back_populates="words")

    word: Mapped[str] = mapped_column(String)
    transcription: Mapped[str | None] = mapped_column(String, nullable=True)
    translate: Mapped[str] = mapped_column(String)
    context: Mapped[str | None] = mapped_column(String, nullable=True)

    pic: Mapped[str | None] = mapped_column(String, nullable=True)
    sound: Mapped[str | None] = mapped_column(String, nullable=True)

    stage: Mapped[int] = mapped_column(Integer, default=0)  # 0 = стадия запоминания
    next_date_time_for_repeat: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        default=now_utc,
    )

    # def get_for_repeat(self,dictionary:'Dictionary'):
    #     ...

    def update_history(self, success: bool) -> None:
        steps = get_next_step_time(self.stage, success)
        self.stage = steps.step
        self.next_date_time_for_repeat = steps.new_date_time


class Skill(AutomatisationDataBase):
    """юзерские навыки"""

    __tablename__ = "skills"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="skills")

    stage: Mapped[int] = mapped_column(Integer, default=0)  # 0 = стадия запоминания

    next_date_time_for_repeat: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        default=now_utc,
    )

    description: Mapped[str] = mapped_column(String)
    instruction: Mapped[str] = mapped_column(String)
    skill_name: Mapped[str] = mapped_column(String, index=True)

    notify_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    notify_already_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # после того как отправили - ставит True, после повторения - снова False

    count_elements: Mapped[int | None] = mapped_column(Integer)  # если ммного например слов рандомно показывать - то сколько

    skill_type: Mapped[SkillType] = mapped_column(SQLEnum(SkillType))

    # ТО ЧТО ДАЛЕЕ - ПОКА НЕ ЮЗАЕМ



    time_show: Mapped[int] = mapped_column(Integer)  # сколько времени показывать
    time_for_remember: Mapped[int] = mapped_column(Integer)  # сколько времени запоминать

    start_depend_of_skill_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("skills.id"),
        nullable=True,
    )

    start_depend_of_skill: Mapped["Skill | None"] = relationship(
        "Skill",
        remote_side="Skill.id",
    )

    def update_history(self, success: bool) -> None:
        steps = get_next_step_time(self.stage, success)
        self.stage = steps.step
        self.next_date_time_for_repeat = steps.new_date_time


class CommonDictionary(AutomatisationDataBase):
    """
    ПОКАЧТО 1 БОТ = 1 СЛОВАРЬ. ТЕ ДЛЯ АНГ ОДИН БОТ, ДЛЯ ВЬЕТ - ДРУГОЙ БОТ И ТД
    """

    __tablename__ = "common_dictionaries"

    name: Mapped[str] = mapped_column(String)
    dictionaries: Mapped[list["Dictionary"]] = relationship(
        "Dictionary",
        back_populates="common_dictionary",
    )
    #
    # user_with_need_notify: Mapped[list["User"]] = relationship(
    #     "User",
    #     secondary="dictionaries",
    #     primaryjoin=lambda: CommonDictionary.id == Dictionary.common_dictionary_id,
    #     secondaryjoin=lambda: and_(
    #         Dictionary.user_id == User.id,
    #         Dictionary.notify_enabled.is_(True),
    #         Dictionary.notify_already_sent.is_(False),
    #         Dictionary.words.has
    #             (
    #             and_(
    #                 WordId.next_date_time_for_repeat <= func.now(),
    #                 WordId.stage > 0,
    #                 )
    #             )
    #     ),
    #     viewonly=True,
    #     lazy="select",
    # )


class Dictionary(AutomatisationDataBase):
    """
    юзерские словари
    """

    __tablename__ = "dictionaries"

    common_dictionary_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("common_dictionaries.id"),
    )
    common_dictionary: Mapped["CommonDictionary"] = relationship(
        "CommonDictionary",
        back_populates="dictionaries",
    )

    words: Mapped[list["Word"]] = relationship(
        "Word",
        back_populates="dictionary",
        cascade="all, delete-orphan",
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String)
    #для повторен:
    ready_words_repeat: Mapped[list["Word"]] = relationship(
        "Word",
        primaryjoin=lambda: and_(
            Dictionary.id == Word.dict_id,
            Word.next_date_time_for_repeat <= func.now(),
            Word.stage > 0,
        ),
        viewonly=True,
        lazy="select",
    )  # слова для повтора

    words_for_memorize: Mapped[list["Word"]] = relationship(
        "Word",
        primaryjoin=lambda: and_(
            Dictionary.id == Word.dict_id,
            Word.stage == 0,  # ← тут
        ),
        viewonly=True,
        lazy="select",
    )

    notify_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_already_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # после того как отправили - ставит True, после повторения - снова False


# ----- USERS -----


def get_notify_status(session: Session,tg_id: int) -> bool:
    user = User.find_by(session, tg_id=str(tg_id)).first()
    return user.notify_for_skills_enabled if user else True

# ----- SKILLS -----

def add_or_update_skill(session: Session,
                        user: User,
                        skill_name: str,
                        count_elements: int | None,
                        time_show: int,
                        time_for_remember: int,
                        skill_type: SkillType,
                        description: str,
                        instruction: str,
                        ) -> Skill:

    skill_instance:Skill = Skill.find_by(session,user_id=user.id, skill_name=skill_name).first()

    if skill_instance is None:
        skill_instance=Skill.add_something(session,
            is_commit=True,
            user_id=user.id,
            skill_name=skill_name,
            count_elements=count_elements,
            time_show=time_show,
            time_for_remember=time_for_remember,
            skill_type=skill_type,
            description=description,
            instruction=instruction,
        )

    else:
        skill_instance.count_elements=count_elements
        skill_instance.time_show=time_show
        skill_instance.time_for_remember=time_for_remember
        skill_instance.type=skill_type
        skill_instance.description=description
        skill_instance.instruction=instruction

    return cast(Skill, skill_instance)


def delete_skill(session: Session, user: User, skill_name: str) -> None:
    Skill.find_by(session,user_id=user.id, skill_name=skill_name).first().delete(session)


def get_list_words_for_memorize_from_db(session,
                                        common_dictionary_id:
                                int, user_id: int,
                                        limit: int = 5,
                                        ) -> list[Word]:
    return (
        session.query(Word)
        .join(Dictionary, Dictionary.id == Word.dict_id)
        .filter(
            Dictionary.common_dictionary_id == common_dictionary_id,
            Dictionary.user_id == user_id,
            Word.stage == 0,
        )
        .limit(limit)
        .all()
    )


def get_skill_for_memorize_db(session, user_id: int, stage_depend_skill_for_get=5) -> Skill | None:
    return (
        session.query(Skill)
        .outerjoin(
            Skill.start_depend_of_skill,
        )
        .filter(
            Skill.user_id == user_id,
            Skill.stage == 0,
            #берем если нет зависмостей от других или зависимость больше
            or_(
                Skill.start_depend_of_skill_id.is_(None),
                Skill.start_depend_of_skill.has(Skill.stage >= stage_depend_skill_for_get),
            ),
        )
        .first()
    )

def add_words(session:Session,
              common_dct: CommonDictionary,
              user: User,
              words: list[WordModel],
              ) -> None:
    dct: Dictionary | None   = Dictionary.find_by(session,
        common_dictionary_id=common_dct.id,
        user_id=user.id,
    ).first()

    if not dct:
        dct = Dictionary.add_something(session,
            common_dictionary_id=common_dct.id,
            user_id=user.id,
            name=common_dct.name,
        )

    for word_model in words:
        word_db = Word.add_something(session,
            dict_id=dct.id,
            word=word_model.word,
            transcription=word_model.transcription,
            translate=word_model.translate,
            context=word_model.context,
        )
        session.add(word_db)

    session.commit()


def get_skill_for_repeat_db(session:Session,user_id: int) -> Skill | None:
    return (
        session.query(Skill)
        .filter(
            Skill.user_id == user_id,
            Skill.stage > 0,
            Skill.next_date_time_for_repeat <= func.now(),
        )
        .first()
    )

def get_users_with_ready_words(session: Session, common_dictionary_id: int) -> list[User]:
    l_us=(
        session.query(User)
        .join(Dictionary, Dictionary.user_id == User.id)
        .join(Word, Word.dict_id == Dictionary.id)
        .filter(
            Dictionary.common_dictionary_id == common_dictionary_id,
            Dictionary.notify_enabled.is_(True),
            Dictionary.notify_already_sent.is_(False),
            Word.next_date_time_for_repeat <= func.now(),
            Word.stage > 0,
        )
        .distinct()
        .all()
    )
    return cast(list[User], l_us)

def create_db() -> None:
    AutomatisationDataBase.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db()
