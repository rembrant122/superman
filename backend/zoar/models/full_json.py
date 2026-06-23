from pydantic import BaseModel

from src.models.cards_models import ResultCards
from src.models.user_info import UserInfoModel
from src.my_enums import PageType


class ResultJson(BaseModel):
    """

    my_info:{
        id:...,
        user_name:...,,#TODO на кл заменить на user_name!!!
        current_avatar:...,#TODO:потом замеить на фронте на меди
        resources:...,
        ...},#???????

    "page_type": page_type,
    "page_title": page_title,
    "data":
            [
                {
                        id:int
                        user_name:Optional[str]
                        is_curator:bool
                        current_avatar: Optional[AvatarModel] = None
                                id:int
                                media:Optional[MediaModel]=None
                                branch_id:int

                        user_resources: ResourcesModel
                                hrony:int
                                hrony_media:MediaModel
                                influence:int
                                influence_media:MediaModel

                                list_user_artefacts: list[Artefact] = []
                        reg_datetime: datetime
                        my_curator_id: Optional[int] = None

                }
            ,
            ...
            ]
"""

    my_info:UserInfoModel
    page_type:PageType
    page_title:str|None=None
    data: list[ResultCards]
