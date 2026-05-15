from datetime import datetime

from pydantic import BaseModel, ConfigDict

from SkillType import SkillType, MyEnum

class StageType(MyEnum):
    REPEAT='REPEAT'
    MEMORIZE='MEMORIZE'

class AutomatisationBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={object: str}
    )

class WordModel(AutomatisationBaseModel):

    id: int
    word: str
    translate: str
    transcription: str | None = None
    context:str| None = None


class DictionaryModel(AutomatisationBaseModel):

    id: int
    # name: str
    words: list[WordModel] = []

class ListWordsModel(AutomatisationBaseModel):

    words: list[WordModel] = []
    stage: StageType

class ResultRepeatWord(AutomatisationBaseModel):

    id_word: int
    result: bool
class ForgotWord(AutomatisationBaseModel):

    id_word: int

class ResultRepeatSkill(AutomatisationBaseModel):

    id_skill: int
    result: bool

class SkillModel(AutomatisationBaseModel):

    id: int
    instruction:str
    description:str
    skill_name: str
    time_show:int
    time_for_remember:int
    type:SkillType


def parse_words_string(value: str) -> list[WordModel] | bool:
    try:
        parts = value.split("\n")

        result: list[WordModel] = []

        for i, part in enumerate(parts, start=1):
            if not part.strip():
                continue

            items = part.split("|")

            if len(items) < 2:
                return False

            result.append(
                WordModel(
                    id=i,
                    word=items[0].strip(),
                    translate=items[1].strip(),
                    transcription=items[2].strip() if len(items) > 2 else None,
                    context=items[3].strip() if len(items) > 3 else None,
                )
            )

        return result

    except Exception:
        return False


class Steps(AutomatisationBaseModel):

    step: int
    new_date_time: datetime
