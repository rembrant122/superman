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

class PageType(MyEnum):
    """
    разделы
    """

    wiki = 'wiki'
    curated = 'curated'  # курируемые -> В БОТ
    community_participants = 'community_participants'  # участники сообщества -> ПОКА НЕТ СООБЩЕСТВ!
    artifacts = 'artifacts'  # артефакты-> ПО УМОЛЧАНИБ ЕСТЬ В MY_INFO
    branches = 'branches' #все доступные ветки->ПОКА ПРОСТО ВСЕ
    my_curator = 'my_curator'  # мой куратор ->В БОТ
    completed_missions = 'completed_missions'  # пройденные миссии ->ПОКА НЕ ДЕЛАЕМ

    my_meetups = 'my_meetups'

    select_branch = 'select_branch'
    avatars = 'avatars'  # ЮЗЕР аватары

    current_quests = 'current_quests'  # текущие квесты + текущий шаг
    quest_participants = 'quest_participants'  # участники квеста ->ПОКА НЕТ СООБЩЕСТВ!
    quest_step='quest_step'#текущий квест и id из ChoiceModel. Сервер может вернуть None=нет следующих шагов


    reg='reg'

class TypeShowCard(MyEnum):

    list_card='list_card'
    carousel= 'carousel'
    one_card='one_card'
    # user_settings='user_settings'

class StepMeetup(MyEnum):

    reg_member='reg_member'
    confirm_come='confirm_come'
    confirm_success='confirm_success'


class QuestsTypes(MyEnum):

    ...

class UserQuestStage(MyEnum):
    appointed='appointed'#назначен
    complete='complete'#завершен
    not_complete='not_complete'#провален
    ...
