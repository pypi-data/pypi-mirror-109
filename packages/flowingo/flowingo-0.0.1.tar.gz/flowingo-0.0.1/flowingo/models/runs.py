import datetime
from typing import Optional, Any

from sqlalchemy import Column, Integer, PickleType, Text, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base
from ..pipelines import get_pipeline_hash
from .pipelines import Pipeline


class Run(Base):
    __tablename__ = 'run'

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id'), index=True)
    pipeline_dump_id = Column(Integer, ForeignKey('pipeline_dump.id'), nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))

    execution_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    start_timestamp = Column(DateTime, nullable=True)
    end_timestamp = Column(DateTime, nullable=True)

    # Relations
    user = relationship("User")
    pipeline = relationship("Pipeline", back_populates="runs")

    def __repr__(self):
        return f'<Run {self.id} for pipeline_id: {self.pipeline_id}>'
