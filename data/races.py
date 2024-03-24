import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Races(SqlAlchemyBase):
    __tablename__ = 'races'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    hero_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("heroes.id"))
    hero = orm.relationship('Hero')
