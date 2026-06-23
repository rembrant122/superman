from pydantic import Field

from src.models.artefact import Artefact
from src.models.basic_models import AutomatisationBaseModel
from src.models.media import MediaModel


class ResourcesModel(AutomatisationBaseModel):
    """

    Хроны и инфы распочковываем на фронте

    """

    list_user_artefacts: list[Artefact] = Field(default_factory=list)
