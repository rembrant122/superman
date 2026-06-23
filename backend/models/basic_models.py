from pydantic import BaseModel, ConfigDict


class AutomatisationBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={object: str}
    )
