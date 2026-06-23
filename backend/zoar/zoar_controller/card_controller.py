from typing import Optional

from pydantic import BaseModel

from db.basic_tables_zoar import Wiki, Branches, Meetup
from db.quests import StepsOfQuest, ListChoiceQuests, Quest
from db.user import User, Avatars
from zoar.models.avatar import AvatarModel, ListAvatarModel
from zoar.models.branhces import ListBranchesModel, BranchModel
from zoar.models.cards_models import ResultCards, ChoiceModel, Card
from zoar.models.meetups import UsersMeetups
from zoar.models.quest import ListQuestsModel, QuestModel, ListUserQuestsModel, UserQuestModel, StepsOfQuestModel
from zoar.models.resources import ResourcesModel
from zoar.models.from_client import IncomeCard
from zoar.models.full_json import ResultJson
from zoar.models.media import MediaModel
from zoar.models.wiki import WikiModel, WikiStructureModel
from my_enums import TypeShowCard, PageType, UserQuestStage
from models.user_info import UserInfoModel

class CardController:

    def __init__(self,my_user_id,income_card:IncomeCard):
        self.income_card=income_card
        self.user_id=my_user_id
        self.user:User=User.find_by_id(self.user_id)

    def route_card(self)->BaseModel:
        result_card:BaseModel|None=None
        match self.income_card.type_card:
            case PageType.wiki:
                result_card=self.wiki()

            case PageType.current_quests:
                result_card=self.get_my_quests() #ВСЕ квесты
            case PageType.quest_step:
                result_card=self.get_quest_next_step()

            # case PageType.quest_participants:
            #     result_card=self.quest_participants()

            case PageType.branches:
                result_card=self.branches()

            case PageType.avatars:
                result_card=self.avatars()
            case PageType.my_meetups:
                result_card=self.my_meetups()
            case PageType.select_branch:
                result_card = self.selected_branch()#присылает аватара по ветке или None


        if not result_card:

            raise Exception(f"No card found for {self.income_card.type_card}")

        return result_card

    def get_quest_next_step(self)->StepsOfQuestModel|None:

        choiced_id=self.income_card.choice_id
        id_quest=self.income_card.id_card

        user_quests=self.user.user_quests
        child=None

        for user_quest in user_quests:
            if user_quest.quest_id==id_quest:
                step_been=user_quest.step_now
                child = next((c for c in step_been.child_links if c.id == choiced_id), None)

        quest_child=child.quest_child

        if quest_child:
            step_next_quest=StepsOfQuestModel.model_validate(quest_child)
            return step_next_quest
        else:
            return None

    @staticmethod
    def user_info(user:User)->UserInfoModel:

        name = user.user_name

        current_avatar = AvatarModel.model_validate(user.current_avatar)
        resources = ResourcesModel.model_validate(user.user_resources)

        my_curator_id=user.my_curator_id

        user_info=UserInfoModel(id=user.id,user_name=name,
                           current_avatar=current_avatar,
                           user_resources=resources,
                                is_curator=user.is_curator,
                                reg_datetime=user.reg_datetime,
                                my_curator_id=my_curator_id)

        return user_info

    def result_json(self, result_card:list[ResultCards],
                    page_title='card')-> ResultJson:

        page_type=self.income_card.type_card

        my_info=self.user_info(self.user)
        result_json=ResultJson(my_info=my_info,
                               page_type=page_type,
                               page_title=page_title,
                               data=result_card)
        return result_json

    def wiki(self)-> ResultCards:

        if self.income_card.id_card is None:
            #начальная страничка вики
            wiki_db:Wiki=Wiki.find_by(head=True).first()
        else:
            wiki_db:Wiki=Wiki.find_by_id(self.income_card.id_card)

        down_wiki_model:list[WikiModel]=[]

        for down_wiki in wiki_db.down_wiki:
            down_wiki_model.append(WikiModel.model_validate(down_wiki))

        wiki=WikiModel.model_validate(wiki_db)
        upper_wiki=WikiModel.model_validate(wiki_db.upper_wiki)
        wiki_full=WikiStructureModel(wiki=wiki,upper_wiki=upper_wiki,down_wiki=down_wiki_model)

        return wiki_full

    @staticmethod
    def get_buttons_links(step_quest:StepsOfQuest)-> list[ChoiceModel]:
        """
        список кнопок формирует
        """
        choice_list: list[ChoiceModel]=[]
        for button in step_quest.child_links:
            choice=ChoiceModel.model_validate(button)
            choice_list.append(choice)
        return choice_list

    def list_quest_cards(self, list_step_quest:list[StepsOfQuest])-> list[Card]:

        list_cards:Optional[list[Card]]=[]

        for quest in list_step_quest:

            media=MediaModel.from_db(quest.media)
            choice_list: list[ChoiceModel] = self.get_buttons_links(quest)
            add_resources=ResourcesModel.model_validate(quest.quest_add_resources)
            card=Card(id=quest.id,media=media,choice_list=choice_list,add_resources=add_resources,start_quest=quest.start_quest)

            list_cards.append(card)
        return list_cards

    @staticmethod
    def list_users_cards(list_users:list[User])-> list[Card]:

        list_cards:Optional[list[Card]]=[]

        for user in list_users:
            media_model:MediaModel|None=None
            if user.current_avatar:
                media_model=MediaModel.from_db(user.current_avatar.media)
            card=Card(id=user.id,media=media_model)
            list_cards.append(card)
        return list_cards

    @staticmethod
    def list_avatars_cards(list_avatars:list[Avatars])-> list[Card]:
        list_cards:Optional[list[Card]]=[]

        for avatar in list_avatars:
            media=MediaModel.from_db(avatar.media)
            branch_name=avatar.branch.media.head_text
            card=Card(id=avatar.id,media=media,additional_text_info=branch_name)
            list_cards.append(card)
        return list_cards

    @staticmethod
    def list_branches_cards(list_branches:list[Branches])-> ListBranchesModel:

        lst_b:list[BranchModel]=[]
        for branch in list_branches:
            branch_model = BranchModel.model_validate(branch)
            lst_b.append(branch_model)
        return ListBranchesModel(list_branches=lst_b)

    @staticmethod
    def list_meetups_cards(list_meetups:list[Meetup])-> list[Card]:
        list_cards:Optional[list[Card]]=[]
        for meetup in list_meetups:
            id=meetup.id
            media=MediaModel.from_db(meetup.media)
            choice=ChoiceModel(id=meetup.id,name_text_button='Выбрать')
            card=Card(id=id,media=media,choice_list=[choice])
            list_cards.append(card)

        return list_cards

    def get_my_quests(self)-> ListUserQuestsModel:

        return self.current_user_quests(self.user,None)

    @staticmethod
    def current_user_quests(user:User, stage: UserQuestStage | None)->ListUserQuestsModel:
        """
        stage=None=> показать все
        """
        list_quest_model=ListUserQuestsModel()

        for user_quest in user.user_quests:
            if user_quest.stage==stage:
                user_quest=UserQuestModel.model_validate(user_quest.quest)
                list_quest_model.list_quests.append(user_quest.quest)

        return list_quest_model

    # def quest_participants(self)->ResultCards:
    #
    #     quest_id=self.income_card.choice_id
    #     users=get_quest_participants(quest_id)
    #     cards=self.list_users_cards(users)
    #
    #     result_card=ResultCards(list_cards=cards)
    #     return result_card

    def choice_branches(self)->ResultCards:
        branches:list[Branches]=Branches.find_by().all()
        cards=self.list_branches_cards(branches)
        result_card=ResultCards(list_cards=cards)
        return result_card

    def branches(self)->ResultCards:

        branches=Branches.find_by().all()

        cards=self.list_branches_cards(branches)
        result_card=ResultCards(list_cards=cards)

        return result_card

    def avatars(self)->ListAvatarModel:

        lst_av=ListAvatarModel()
        for avatar in self.user.list_avatars:
            av_model=AvatarModel.model_validate(avatar)
            lst_av.append(av_model)
        return lst_av

    def my_meetups(self)->UsersMeetups:
        return UsersMeetups.get_from_db(self.user)

    def selected_branch(self)->AvatarModel|None:
        """
        создание аватара если его нет по ветке
        смена


        """

        branch_id=self.income_card.choice_id

        av_model=None

        for av in self.user.list_avatars:
            if av.branch_id==branch_id:
                av_model=AvatarModel.model_validate(av)

        return av_model
