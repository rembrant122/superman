from datetime import datetime

from pydantic import BaseModel, Field

from src.models.basic_models import AutomatisationBaseModel
from src.models.quest import QuestModel


class SettingModel(BaseModel):
    id:int
    user_name:str
    new_branch_id:int
