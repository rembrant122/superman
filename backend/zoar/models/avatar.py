from typing import Optional

from pydantic import Field, BaseModel

from models.basic_models import AutomatisationBaseModel
from models.branhces import BranchModel
from models.media import MediaModel


class AvatarModel(AutomatisationBaseModel):

    id:int
    media:Optional[MediaModel]=None
    branch:BranchModel

class ListAvatarModel(BaseModel):

    list_avatars:list[AvatarModel]=Field(default_factory=list)
