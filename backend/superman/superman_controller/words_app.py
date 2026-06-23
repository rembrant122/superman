from datetime import datetime, UTC
from typing import TypeVar

from apiflask import APIBlueprint

from app_flask.api_post import api_route
from app_flask.auth_user import get_user
from app_flask.get_dict_db import get_dict_db
from app_flask.save_and_send_app import send_message
from db.db_all import Word, get_list_words_for_memorize_from_db
from db.db_basic import session_scope
from superman.models.models_superman import AutomatisationBaseModel, WordModel, WordId, ListWordsModel, ListWordsIdModel
from settings import COMMON_DIC_ID
from steps import get_next_step_time
from typing import cast

T = TypeVar("T", bound=AutomatisationBaseModel)

words_blueprint = APIBlueprint("words", __name__)

@api_route(words_blueprint,"/get_list_words_for_repeat",
    method="get",output_model=ListWordsModel)

def get_list_words_for_repeat()->ListWordsModel|dict:
    with session_scope() as session:
        dict_db = get_dict_db(session)

        # if dict_db is None:
        #     return send_message()

        words:list[WordModel]=[]

        for word_db in dict_db.ready_words_repeat:
            word=WordModel.model_validate(word_db)
            words.append(word)

        return send_message(ListWordsModel(words=words))


@api_route(words_blueprint,
    "/get_list_words_for_memorize",
    method="get",
    output_model=ListWordsModel,)

def get_list_words_for_memorize()->ListWordsModel|dict:
    with session_scope() as session:
        # dict_db = get_dict_db(session)
        #
        # if dict_db is None:
        #     return send_message()

        user = get_user(session)
        words = get_list_words_for_memorize_from_db(session, COMMON_DIC_ID, user.id) # берет 5 слов
        words_models = [WordModel.model_validate(word) for word in words]

        return send_message(ListWordsModel(words=words_models))


@api_route(
    words_blueprint,
    "/save_result_memorize",
    input_model=ListWordsIdModel,
)
def save_result_memorize(words_models: ListWordsIdModel):
    with session_scope() as session:
        for word_id in words_models.words_id:
            word_db: Word | None = Word.find_by_id(session, word_id)
            if word_db is not None:
                word_db.stage += 1
                word_db.next_date_time_for_repeat = datetime.now(UTC)

    return send_message()

@api_route(
    words_blueprint,
    "/save_result_repeat_word",
    input_model=WordId,
)

def save_result_repeat_word(word_model: WordId):
    with session_scope() as session:
        word: Word | None = Word.find_by_id(session, word_model.id_word)

        step_now = cast(int, word.stage)
        new_step = get_next_step_time(step_now, word_model.result)
        word.stage = new_step.step
        word.next_date_time_for_repeat = new_step.new_date_time

    return send_message()
