from datetime import datetime

from pydantic import BaseModel

from src.db.user import User
from src.models.basic_models import AutomatisationBaseModel
from src.models.media import MediaModel
from src.models.user_info import UserInfoModel
from src.my_enums import StepMeetup



class MeetupUsers(AutomatisationBaseModel):
    user:UserInfoModel
    step_user:StepMeetup

    ...
class MeetupModel(AutomatisationBaseModel):

    media:MediaModel
    datetime_start:datetime
    place:str
    is_online:bool
    master:UserInfoModel
    meetup_users:list[MeetupUsers]

class UsersMeetups(BaseModel):
    list_meetups:list[MeetupModel]

    @classmethod
    def get_from_db(cls,user:User)->'UsersMeetups':
        lst_meetups:list[MeetupModel] = []
        for meetup_db in user.meetup_user:
            lst_meetups.append(MeetupModel.model_validate(meetup_db.meetup))
        return cls(list_meetups=lst_meetups)
