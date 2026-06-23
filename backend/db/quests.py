from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.db_basic import AutomatisationDataBase
from db.table_names import TableNames

if TYPE_CHECKING:

    from basic_tables_zoar import Media, Meetup,Branches
    from db.resourses import Resources, Artefacts
    from user import UserQuest


# class StepQuestArtefacts(MyDataBase):
#
#     """Артефакты которые могут быть выданы после ШАГА квеста"""
#
#     __tablename__ = TableNames.step_quest_artefacts
#
#     step_quest_id: Mapped[int] = mapped_column(ForeignKey(TableNames.steps_of_quest.id))
#     step_quest: Mapped['StepsOfQuestModel'] = relationship('StepsOfQuestModel', uselist=False, back_populates='step_quest_artefacts')
#
#     artefact_id: Mapped[int] = mapped_column(ForeignKey(TableNames.artefacts.id))
#     artefact: Mapped['Artefacts'] = relationship('Artefacts', uselist=False)


class ListChoiceQuests(AutomatisationDataBase):

    """
    по сути - спиок кнопок
    """

    __tablename__ = TableNames.list_choice_quests

    quest_parent_id: Mapped[int] = mapped_column(ForeignKey(TableNames.steps_of_quest.id))
    quest_child_id: Mapped[int] = mapped_column(ForeignKey(TableNames.steps_of_quest.id))  # следующий квест

    text_button: Mapped[str] = mapped_column(String)

    quest_parent: Mapped["StepsOfQuest"] = relationship(
        "StepsOfQuest",
        foreign_keys=lambda: [ListChoiceQuests.quest_parent_id],
        back_populates="child_links",
    )

    # отношение к «дочернему» квесту
    quest_child: Mapped["StepsOfQuest"] = relationship(
        "StepsOfQuest",
        foreign_keys=lambda: [ListChoiceQuests.quest_child_id],
        back_populates="parent_links",
    )

class StepsOfQuest(AutomatisationDataBase):

    """
    """

    __tablename__ = TableNames.steps_of_quest

    quest_id=mapped_column(ForeignKey(TableNames.quests.id))
    quest: Mapped['Quest'] = relationship('Quest')

    start_quest: Mapped[bool] = mapped_column(Boolean)
    finish_quest: Mapped[bool] = mapped_column(Boolean) # для начисления очков

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

    quest_add_resources_id: Mapped[int] = mapped_column(ForeignKey(TableNames.resources.id))
    quest_add_resources: Mapped['Resources'] = relationship('Resources')# имеется ввиду за ШАГ квеста

    child_links: Mapped[list['ListChoiceQuests']] = relationship(
        'ListChoiceQuests',
        foreign_keys=lambda: [ListChoiceQuests.quest_parent_id],
        back_populates='quest_parent',
        cascade='all, delete-orphan'
    )

    parent_links: Mapped[list['ListChoiceQuests']] = relationship(
        'ListChoiceQuests',
        foreign_keys=lambda: [ListChoiceQuests.quest_child_id],
        back_populates='quest_child',
        cascade='all, delete-orphan'
    )#это поле наверно не нужно просто

    # list_meetups: Mapped[list['Meetup']] = relationship('Meetup', back_populates='step_quest',uselist=False)
    #
    # step_quest_artefacts: Mapped[list['StepQuestArtefacts']] = relationship(
    #     'StepQuestArtefacts',
    #     back_populates='step_quest',
    #     cascade='all, delete-orphan'
    # )

    @classmethod
    def get_quest_by_parent_id(cls, parent_id: int):
        return cls.find_by(id=parent_id).first()

class Quest(AutomatisationDataBase):

    __tablename__ = TableNames.quests

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

    branch_id: Mapped[int | None] = mapped_column(
        ForeignKey(TableNames.branches.id),
        nullable=True,
    )

    branches: Mapped['Branches | None'] = relationship('Branches')

    participants: Mapped[list['UserQuest']] = relationship('UserQuest', back_populates='step_quest')
