from db.user import User
from db.db_basic import SessionLocal
from settings import MOISEY_TG_ID

USER=MOISEY_TG_ID

def get_tst_user() -> User:
    with SessionLocal() as session:
        return User.find_by(session, tg_id=str(USER)).first()
