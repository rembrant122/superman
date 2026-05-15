from enum import Enum



class MyEnum(str, Enum):
    @property
    def __str__(self) -> str:
        return self.value

class SkillType(MyEnum):

    # WORD='WORD'#слово-перевод
    LIST_WORDS_FOR_MEMORIZ= 'LIST_WORDS_FOR_MEMORIZ'#список слов чтобы запомнить
    LIST_WORD_FOR_IMAGENATED='LIST_WORD_FOR_IMAGENATED'#список слов чтобы представить
    EXERCISE='EXERCISE'#любое упраженение
