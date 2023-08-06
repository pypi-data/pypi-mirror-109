import datetime

from sqlalchemy import Column, Integer, PickleType, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from .base import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)

