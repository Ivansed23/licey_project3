import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Hero(SqlAlchemyBase):
    __tablename__ = 'heroes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             index=True, unique=True)
    race_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("races.id"))
    class_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("classes.id"))

    races = orm.relationship('Races')
    classes = orm.relationship('Classes')
