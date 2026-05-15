from typing import TypeVar

from apiflask import APIBlueprint
from sqlalchemy.orm import Session

from app_flask.api_post import api_route
from app_flask.auth_user import get_user
from app_flask.save_and_send_app import send_message
from db.db_all import Dictionary, User, Word, get_list_words_for_memorize
from db.db_basic import session_scope
from models import AutomatisationBaseModel, DictionaryModel, ResultRepeatWord, WordModel, ForgotWord
from settings import COMMON_DIC_ID
from steps import get_next_step_time
from typing import cast

T = TypeVar("T", bound=AutomatisationBaseModel)

words_blueprint = APIBlueprint("words", __name__)

def get_dict_db(session: Session) -> Dictionary | None:
    user: User = get_user(session)
    return Dictionary.find_by(
        session,
        user_id=user.id,
        common_dictionary_id=COMMON_DIC_ID,
    ).first()

@api_route(words_blueprint,"/get_list_words_for_repeat",
    method="get",output_model=DictionaryModel)
def get_list_words_for_repeat():
    with session_scope() as session:
        dict_db = get_dict_db(session)

        if dict_db is None:
            return send_message()

        words:list[WordModel]=[]

        for word_db in dict_db.words_for_memorize:
            word=WordModel.model_validate(word_db)
            words.append(word)

        dict_model = DictionaryModel(
            id=dict_db.id,
            words=words,
        )
        return send_message(dict_model)


@api_route(words_blueprint,
    "/get_list_words_for_memorize_eng",
    method="get",
    output_model=DictionaryModel,)
def get_list_words_for_memorize_eng():
    with session_scope() as session:
        dict_db = get_dict_db(session)

        if dict_db is None:
            return send_message()

        user = get_user(session)
        words = get_list_words_for_memorize(session, COMMON_DIC_ID, user.id)
        words_model = [WordModel.model_validate(word) for word in words]

        dict_model = DictionaryModel(
            id=dict_db.id,
            words=words_model,
        )
        return send_message(dict_model)


@api_route(
    words_blueprint,
    "/save_result_memorize",
    input_model=DictionaryModel,
)
def save_result_memorize(dict_model: DictionaryModel):
    with session_scope() as session:
        for word_model in dict_model.words:
            word_db: Word | None = Word.find_by_id(session, word_model.id)
            if word_db is not None:
                word_db.stage += 1

    return send_message()


@api_route(
    words_blueprint,
    "/save_result_repeat_word",
    input_model=ForgotWord,
)

def save_result_repeat_word(data: ForgotWord):
    with session_scope() as session:
        word: Word | None = Word.find_by_id(session, data.id_word)

        # if word is None:
        #     return send_message()
        step_now = cast(int, word.stage)

        new_step = get_next_step_time(step_now, False)
        word.stage = new_step.step
        word.next_date_time_for_repeat = new_step.new_date_time

    return send_message()
