import datetime
from typing import Optional, Any

from sqlalchemy import Column, Integer, PickleType, Text, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base
from ..pipelines import get_pipeline_hash


class PipelineTag(Base):
    __tablename__ = 'pipeline_tag'

    name = Column(String(64), primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id'), primary_key=True)

    # Relations
    pipeline = relationship("Pipeline", back_populates="tags")

    def __repr__(self):
        return f'<Tag {self.name} for pipeline_id: {self.pipeline_id}>'


class PipelineDump(Base):
    __tablename__ = 'pipeline_dump'

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id'), index=True)

    pickle = Column(PickleType())
    pipeline_hash = Column(String(64), unique=True)

    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relations
    pipeline = relationship("Pipeline", foreign_keys=[pipeline_id])

    def __init__(self, pipeline_dict: Optional[dict], *args, **kwargs):
        super(PipelineDump, self).__init__(*args, **kwargs)
        if pipeline_dict:
            self.pipeline_hash = get_pipeline_hash(pipeline_dict)
            self.pickle = pipeline_dict

    def __repr__(self):
        return f'<PipelineDump {self.id}: pipeline_id {self.pipeline_id}>'


class Pipeline(Base):
    __tablename__ = 'pipeline'

    id = Column(Integer, primary_key=True)  # TODO: uuid

    # Header
    title = Column(String(128))
    description = Column(Text)

    # Properties
    sub = Column(Boolean, default=False)
    concurrency = Column(Integer, default=None, nullable=True)

    # Running info
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Tech info
    dump_id = Column(Integer, ForeignKey('pipeline_dump.id'))
    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    filepath = Column(String(512), unique=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    # Relations
    author = relationship("User")
    runs = relationship("Run", cascade='all,delete-orphan', back_populates="pipeline")
    tags = relationship("PipelineTag", cascade='all,delete-orphan', back_populates="pipeline")
    dump = relationship("PipelineDump", foreign_keys=[dump_id], uselist=False, post_update=True)
    dumps = relationship("PipelineDump", foreign_keys=[PipelineDump.pipeline_id], cascade='all,delete-orphan', back_populates="pipeline")

    def __init__(self, pipeline: Optional[dict] = None, *args: Any, **kwargs: Any):
        super(Pipeline, self).__init__(*args, **kwargs)
        if pipeline:
            self._update_from_dict(pipeline)

    def _update_from_dict(self, pipeline: dict) -> None:
        self.title = pipeline['title']

        if 'description' in pipeline:
            self.title = pipeline['description']
        # if 'tags' in pipeline:
        #     for pipeline['tags']

        if 'properties' in pipeline:
            properties = pipeline['properties']

            if 'sub' in properties:
                self.sub = properties['sub']
            if 'concurrency' in properties:
                self.concurrency = properties['concurrency']

    @property
    def pipeline(self):
        return self.dump.pickle

    def __repr__(self):
        return f"<Pipeline: {self.id}: title: {self.title}>"

