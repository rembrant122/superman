from datetime import datetime
from typing import Optional


from src.models.avatar import AvatarModel
from src.models.resources import ResourcesModel
from src.models.basic_models import AutomatisationBaseModel

class UserInfoModel(AutomatisationBaseModel):
    """
    это видимо для других участников в том числе!
    """

    id:int
    user_name:Optional[str]
    is_curator:bool
    current_avatar: Optional[AvatarModel] = None
    user_resources: ResourcesModel
    reg_datetime: datetime
    my_curator_id: int|None = None

# class UserInfoCurator(BaseModel):
#
#     my:UserInfoModel
#     my_curator: Optional[UserInfoModel] = None
#     my_supervised: list[UserInfoModel] = []
