from sqlalchemy.orm import Session

from app_flask.auth_user import get_user
from db.db_all import Dictionary
from db.user import User
from settings import COMMON_DIC_ID


def get_dict_db(session: Session) -> Dictionary | None:
    user: User = get_user(session)
    return Dictionary.find_by(
        session,
        user_id=user.id,
        common_dictionary_id=COMMON_DIC_ID,
    ).first()
