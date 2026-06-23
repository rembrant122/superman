from typing import Optional

from pydantic import BaseModel

from models.basic_models import AutomatisationBaseModel
from models.media import MediaModel


class BranchModel(AutomatisationBaseModel):

    id:int
    media:Optional[MediaModel]=None

    # my_curator:UserTgModel


class ListBranchesModel(BaseModel):

    list_branches:list[BranchModel]
