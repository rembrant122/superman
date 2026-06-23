import random
from pathlib import Path

from enums import SkillType
from db.db_all import Skill
from superman.models.models_superman import  SkillModel
from settings import UNIQUE_RUSSIAN_WORDS_PATHS


def get_random_words(file: Path, count: int = 20) -> list[str]:
    words = [
        line.strip()
        for line in file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    return random.sample(words, min(count, len(words)))


def prepare_skills(skill:Skill) -> SkillModel:

    is_need_words:bool=False

    match skill.skill_type:
        case SkillType.LIST_WORDS_FOR_MEMORIZ:
            is_need_words = True
        case SkillType.LIST_WORD_FOR_IMAGENATED:
            is_need_words = True
        case SkillType.EXERCISE:
            is_need_words = False

    counts_items=skill.count_elements
    words = get_random_words(Path(UNIQUE_RUSSIAN_WORDS_PATHS), counts_items)

    skill_model = SkillModel.model_validate(skill)

    if is_need_words:
        skill_model.items = words

    return skill_model
