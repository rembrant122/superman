from typing import Optional

from pydantic import BaseModel, Field

from models.basic_models import AutomatisationBaseModel
from models.media import MediaModel


class Artefact(AutomatisationBaseModel):

    id: int
    media: Optional[MediaModel] = None

class ListArtefactsModel(BaseModel):
    list_artefact:list[Artefact]=Field(default_factory=list)
