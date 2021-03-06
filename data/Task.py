import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    complete = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    description = sqlalchemy.Column(sqlalchemy.String, default="")
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    files = sqlalchemy.Column(sqlalchemy.String, default="")


