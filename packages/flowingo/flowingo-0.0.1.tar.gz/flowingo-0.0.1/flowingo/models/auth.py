import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base


from datetime import datetime
import uuid
import typing as tp

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base


# # RBAC model of permissions
# class Role(Base):
#     __tablename__ = "roles"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String, unique=True)
#
#     # relations
#     users = relationship("User", uselist=True, back_populates="role")
#
#     def __repr__(self) -> str:
#         return f'<Role {self.id}: level {self.level} title {self.title}>'


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    # role = Column(Integer, ForeignKey('role.id'))
    username = Column(String(64), index=True, unique=True)
    pass_hash = Column(String(128))

    # relations
    # roles = relationship("Role", uselist=True, back_populates="users")

    def __init__(self, password: tp.Optional[str] = None, *args: tp.Any, **kwargs: tp.Any):
        super(User, self).__init__(*args, **kwargs)
        if password:
            self.password = password  # type: ignore

    @property
    def password(self) -> tp.NoReturn:
        raise ValueError("password is write only.")

    @password.setter
    def password(self, password: str) -> None:
        self.pass_hash = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        return generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pass_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.username}>'
