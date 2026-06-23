from typing import Optional

from pydantic import BaseModel, Field

from src.models.artefact import ListArtefactsModel
from src.models.basic_models import AutomatisationBaseModel
from src.models.choice_model import ChoiceModel
from src.models.resources import ResourcesModel
from src.models.media import MediaModel
from src.my_enums import UserQuestStage


class StepsOfQuestModel(AutomatisationBaseModel):

    id:int
    start_quest:bool
    finish_quest:bool
    media:MediaModel
    list_artefacts:ListArtefactsModel
    child_links:list[ChoiceModel]
    quest_add_resources:ResourcesModel # имеется ввиду за ШАГ квеста

class QuestModel(AutomatisationBaseModel):

    id:int
    media:Optional[MediaModel]=None

class UserQuestModel(AutomatisationBaseModel):

    quest:QuestModel
    step_now:StepsOfQuestModel
    stage:UserQuestStage

class ListQuestsModel(BaseModel):

    list_quests:list[QuestModel]=Field(default_factory=list)

class ListUserQuestsModel(BaseModel):

    list_user_quests:list[UserQuestModel]=Field(default_factory=list)
