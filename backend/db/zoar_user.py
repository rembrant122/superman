import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Integer, String, Text, and_, func, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from db.quests import Quest, StepsOfQuest
from db.resourses import Resources
from db.basic_tables_zoar import Branches, Media, Meetup
from enums import StepMeetup, UserQuestStage
from db.table_names import TableNames
from db.db_basic import AutomatisationDataBase

if TYPE_CHECKING:
    from db.user import User


class MeetupUsers(AutomatisationDataBase):

    """список игроков на встрече"""

    __tablename__ = TableNames.meetup_users

    meetup_id: Mapped[int] = mapped_column(ForeignKey(TableNames.meetups.id))
    meetup: Mapped['Meetup'] = relationship('Meetup', uselist=False, back_populates='meetup_users')

    user_id: Mapped[int] = mapped_column(ForeignKey(TableNames.user.id))
    user: Mapped['User'] = relationship('User',back_populates='meetup_user',uselist=False)

    step_user:Mapped[StepMeetup] = mapped_column(SQLEnum(StepMeetup))
    # quest_type: Mapped[QuestsTypes] = mapped_column(SQLEnum(QuestsTypes), nullable=False)#TODO???


class UserQuest(AutomatisationDataBase):

    __tablename__ = TableNames.user_quests

    user_id: Mapped[int] = mapped_column(ForeignKey(TableNames.user.id))
    quest_id: Mapped[int] = mapped_column(ForeignKey(TableNames.quests.id))

    user: Mapped['User'] = relationship('User', uselist=False, back_populates='user_quests')
    quest: Mapped['Quest'] = relationship('Quest', uselist=False, back_populates='participants')

    stage:Mapped[UserQuestStage] = mapped_column(SQLEnum(UserQuestStage))

    step_now_id:Mapped[int]=mapped_column(ForeignKey(TableNames.steps_of_quest.id))
    step_now:Mapped['StepsOfQuest'] = relationship('StepsOfQuest', uselist=False)

class UserStepQuest(AutomatisationDataBase):
    __tablename__ = "user_step_quests"

def reg_user_by_tg_id(tg_id: str,curator_id)->"User":

    resource = Resources.add_something(is_commit=False)

    #    SQLAlchemy сам подставит FK в поле resources_id
    user = User.add_something(
        is_commit=False,
        tg_id=tg_id,
        user_resources=resource,# <-- вот так через relationship
        my_curator_id=curator_id
    )

    return user

class Avatars(AutomatisationDataBase):
    __tablename__ = TableNames.avatars

    head: Mapped[bool] = mapped_column(Boolean, default=False)

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

    user_id: Mapped[int] = mapped_column(ForeignKey(TableNames.user.id))
    user: Mapped['User'] = relationship(
        'User',
        back_populates='list_avatars',
        foreign_keys=[user_id]
    )

    branch_id: Mapped[int] = mapped_column(ForeignKey(TableNames.branches.id))
    branch: Mapped['Branches'] = relationship('Branches', uselist=False)


    @classmethod
    def new_avatar_db(cls,branch:'Branches',user:"User")-> 'Avatars':
        media_avatar_db = Media.add_something()

        avatar= Avatars.add_something(branch=branch, media=media_avatar_db,user=user)
        return avatar

class UserZoar(AutomatisationDataBase):
    __abstract__ = True


    my_curator_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey(TableNames.user.id),
        nullable=True,  # разрешаем NULL
    )

    my_curator: Mapped['User'] = relationship('User', remote_side=lambda: [User.id], uselist=False,back_populates='supervised')
    is_curator:Mapped[bool]=mapped_column(Boolean, default=False)

    supervised: Mapped[list['User']] = relationship(
        'User',
        foreign_keys=[my_curator_id],
        back_populates='my_curator'
    )

    user_name: Mapped[Optional[str]] = mapped_column(Text)

    reg_datetime: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc)) # type: ignore

    first_time: Mapped[bool] = mapped_column(Boolean, default=True)

    user_resources_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(TableNames.resources.id),
        nullable=True
    )
    user_resources: Mapped['Resources'] = relationship('Resources')

    meetup_user: Mapped[list['MeetupUsers']] = relationship('MeetupUsers', back_populates='user')

    current_avatar_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey(TableNames.avatars.id), nullable=True)
    current_avatar: Mapped["Avatars | None"] = relationship(
        "Avatars",
        foreign_keys=[current_avatar_id],
        uselist=False
    )

    # Здесь внешним ключом является столбец Avatars.user_id, который указывает владельца аватара.
    list_avatars: Mapped[list["Avatars"]] = relationship(
        "Avatars",
        back_populates="user",
        # Используем lambda для отложенной оценки внешнего ключа,
        # чтобы избежать проблемы круговых импортов, если порядок определения классов не позволяет
        foreign_keys=lambda: [Avatars.user_id]
    )
    user_quests: Mapped[list['UserQuest']] = relationship('UserQuest', back_populates='user')

    ...
