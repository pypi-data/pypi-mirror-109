import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


path = pathlib.Path('.tmp/database/')
path.mkdir(exist_ok=True)
engine = create_engine(f"sqlite:///{path.absolute()}/sqlite.db", echo=False, future=True)

Session = sessionmaker(engine, future=True)


Base = declarative_base()


def init():
    print('Really creating...')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Created.')


def migrate():
    raise NotImplementedError()


def info():
    raise NotImplementedError()
