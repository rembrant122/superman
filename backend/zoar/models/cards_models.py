# from abc import ABC
#
# from pydantic import BaseModel
#
# from src.models.media import MediaModel
# from src.models.basic_models import AutomatisationBaseModel
# from src.models.resources import ResourcesModel
# from src.my_enums import TypeShowCard
#
# class ChoiceModel(AutomatisationBaseModel):
#
#     id:int
#     text_button:str
#
#
# class Card(BaseModel,ABC):
#
#     id: int
#     media: MediaModel
#
#     # choice_list: list[ChoiceModel]|None = None
#     # additional_text_info:str|None = None
#     # add_resources: ResourcesModel | None = None
#     #
#     # start_quest:bool|None = None
#     # finish_quest:bool|None = None
#
# class QuestCard(Card):
#
#     info
#     ...
#
# class QuestStepCard(Card):
#     ...
#
#
#
# class ResultCards(BaseModel):
#
#     """
#     """
#
#     list_cards: list[Card]
#     # type_show_card: TypeShowCard
