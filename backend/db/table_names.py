from enum import StrEnum

class TableNames(StrEnum):
    media = 'media'

    resources = 'resources'
    artefacts = 'artefacts'
    special_resources= 'special_resources'

    branches = 'branches'
    wiki = 'wiki'
    meetups = 'meetups'

    quests = 'quests'
    steps_of_quest = 'steps_of_quest'
    step_quest_artefacts='step_quest_artefacts'


    quest_artefacts = 'quest_artefacts'
    list_choice_quests = 'list_choice_quests'
    user = 'users'
    avatars = 'avatars'
    meetup_users = 'meetup_users'
    list_artefacts = 'list_artefacts'
    user_quests = 'user_quests'


    @property
    def id(self) -> str:
        return f'{self}.id'

    @property
    def user_id(self) -> str:
        return f'{self}.user_id'
