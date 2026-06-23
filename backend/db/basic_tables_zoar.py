from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_database import MyDataBase, engine, Base
from table_names import TableNames

if TYPE_CHECKING:
    from user import User,MeetupUsers
    from resourses import Resources


class Meetup(MyDataBase):
    """
    пока вся инфа о месте и тд - кладем в медиа чтообы отобразить на фроенте
    """
    __tablename__ = TableNames.meetups

    # step_quest_id: Mapped[int] = mapped_column(ForeignKey(TableNames.steps_of_quest.id))
    # step_quest: Mapped['StepsOfQuestModel'] = relationship('StepsOfQuestModel', uselist=False, back_populates='list_meetups')

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media:Mapped['Media']=relationship('Media')

    datetime_start: Mapped[datetime] = mapped_column(DateTime)
    place: Mapped[str] = mapped_column(Text)

    is_online: Mapped[bool] = mapped_column(Boolean, default=False)

    master_id: Mapped[int] = mapped_column(ForeignKey(TableNames.user.id))
    master: Mapped['User'] = relationship('User', uselist=False)#ведущий мероприятия

    meetup_users: Mapped[list['MeetupUsers']] = relationship('MeetupUsers', back_populates='meetup')

    add_resources_id: Mapped[int] = mapped_column(ForeignKey(TableNames.resources.id))
    add_resources: Mapped['Resources'] = relationship('Resources')


class Branches(MyDataBase):

    __tablename__=TableNames.branches

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

class Wiki(MyDataBase):
    __tablename__ = TableNames.wiki

    head: Mapped[bool] = mapped_column(Boolean, default=False)

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

    upper_wiki_id: Mapped[int | None] = mapped_column(
        ForeignKey(TableNames.wiki.id),
        nullable=True
    )
    upper_wiki: Mapped['Wiki | None'] = relationship(
        'Wiki',
        remote_side=lambda: [Wiki.id],
        back_populates='down_wiki',
        uselist=False
    )
    down_wiki: Mapped[list['Wiki']] = relationship(
        'Wiki',
        back_populates='upper_wiki'
    )

class Media(MyDataBase):
    __tablename__ = TableNames.media

    head_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    short_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

if __name__ == '__main__':
    # Создание таблицы
    Base.metadata.create_all(bind=engine)
