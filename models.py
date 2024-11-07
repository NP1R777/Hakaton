from datetime import datetime
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Boolean, String, VARCHAR, TIMESTAMP, DATETIME
from sqlalchemy import DATE, ARRAY, ForeignKey

convention = {
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    pass

Base.metadata = MetaData(naming_convention=convention)

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    username: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    password_hash: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    preferences: Mapped[list] = mapped_column(ARRAY(Integer))
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)


class GroupsEvent(Base):
    __tablename__ = "group_event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR)


class UsersGroup(Base):
    __tablename__ = "user_group"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    main_user: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    group_members: Mapped[list] = mapped_column(ARRAY(Integer))


class Events(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("group_event.id"), nullable=False)
    external_url: Mapped[int] = mapped_column(VARCHAR)
    date_start: Mapped[str] = mapped_column(DATE)
    date_end: Mapped[str] = mapped_column(DATE)
    location: Mapped[str] = mapped_column(String)
    is_cyclically: Mapped[bool] = mapped_column(Boolean)


class UserToEvent(Base):
    __tablename__ = "user_to_event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("event.id"), nullable=False)
