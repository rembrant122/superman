
from src.db.basic_tables import * # содержит Artefacts/Branches/Media/...# noqa: F401

from db.db_basic import Base, engine
from quests import *# noqa: F401
from user import *# noqa: F401

Base.metadata.create_all(bind=engine)
