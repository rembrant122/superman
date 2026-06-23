from typing import Optional

from src.db.basic_tables import Media
from src.models.basic_models import AutomatisationBaseModel


class MediaModel(AutomatisationBaseModel):

    id: int
    head_text : Optional[str]=None

    text: Optional[str]=None
    short_text: Optional[str]=None
    image: Optional[str]=None
    video: Optional[str]=None
    audio: Optional[str]=None

    @classmethod
    def from_db(cls, media:Media) -> "MediaModel":
        return cls.model_validate(media)
    def to_db(self)->Media:
        data=self.model_dump(exclude={"id"},exclude_none=True)
        media_db = Media.add_something(**data)
        return media_db
