import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Stations(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'stations'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    station = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    yandex_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)