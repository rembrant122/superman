from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from basic_tables import Media
from my_database import MyDataBase
from table_names import TableNames


class Artefacts(MyDataBase):

    __tablename__ = TableNames.artefacts

    media_id: Mapped[int] = mapped_column(ForeignKey(TableNames.media.id))
    media: Mapped['Media'] = relationship('Media')

class ListArtefacts(MyDataBase):

    __tablename__ = TableNames.list_artefacts

    resources_id: Mapped[int] = mapped_column(ForeignKey(TableNames.resources.id))

    count:Mapped[int] = mapped_column(Integer, default=1)

    artefact_id: Mapped[int] = mapped_column(ForeignKey(TableNames.artefacts.id))  # =

    artefact: Mapped['Artefacts'] = relationship('Artefacts', uselist=False)

class Resources(MyDataBase):
    """
    ХРАНИЛИЩЕ ресурсов для чего либо:
        юзеров
        оплата квесты
        и тд

    """

    __tablename__ = TableNames.resources

    list_user_artefacts: Mapped[list['ListArtefacts']] = relationship('ListArtefacts')
