import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    strong_points = sqlalchemy.Column(sqlalchemy.String)
    weak_points = sqlalchemy.Column(sqlalchemy.String)
    primary_stat = sqlalchemy.Column(sqlalchemy.String)
    class_features = sqlalchemy.Column(sqlalchemy.String)
    weapon_proficiencies = sqlalchemy.Column(sqlalchemy.String)
    tool_proficiencies = sqlalchemy.Column(sqlalchemy.String)
    skill_proficiencies = sqlalchemy.Column(sqlalchemy.String)

    hero = orm.relationship('Hero', back_populates='classes')
    races = orm.relationship('Races', back_populates='classes')
