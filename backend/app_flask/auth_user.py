from flask import request

from db.db_all import User
from sqlalchemy.orm import Session

def get_user(session:Session) -> User:
    header = request.headers.get("Authorization", "")

    if not header.startswith("Bearer "):
        raise ValueError("No token")

    token = header.removeprefix("Bearer ").strip()

    user = User.find_by(session,token=token).first()

    if not user:
        raise ValueError("User not found")

    return user
