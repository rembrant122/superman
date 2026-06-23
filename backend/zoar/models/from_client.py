from pydantic import BaseModel

from models.media import MediaModel
from my_enums import MyEnum, PageType


class IncomeCard(BaseModel):
    """
        тип
        текущ юзер
        вариант
        id карточки
    """

    type_card:PageType
    id_card: int | None = None# НА которой мы находимся
    user_id:int
    choice_id:int#некий ВЫБОР

    media:MediaModel|None=None

class TypeCuratorChoice(MyEnum):

    MEETUP="MEETUP"
    QUEST="QUEST"

class CuratorChoice(BaseModel):

    type_curator_choice:TypeCuratorChoice

    user_id:int#куратора
    list_quests_id:list[int]
    list_user_supervised_id:list[int]

class Avatar(BaseModel):

    media:MediaModel
    user_id:int
    avatar_id:int
