import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)

    hero = orm.relationship('Hero', back_populates='classes')
    races = orm.relationship('Races', back_populates='classes')
