import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Cities(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cities'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    yandex_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)