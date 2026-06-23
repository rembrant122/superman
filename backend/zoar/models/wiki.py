from typing import Optional

from pydantic import BaseModel, Field

from src.models.basic_models import AutomatisationBaseModel
from src.models.media import MediaModel



class WikiModel(AutomatisationBaseModel):

    id:int
    media:Optional[MediaModel]=None

class WikiStructureModel(BaseModel):

    """
    передаем сам раздел и список нижележащих разделов (полностью, с медиа сразу)
    """

    wiki:WikiModel|None=None
    upper_wiki:WikiModel|None=None
    down_wiki:list[WikiModel]=Field(default_factory=list)
