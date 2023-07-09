from typing import Optional

from sqlalchemy import String, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from auria.database.SQLAlchemyDatabase import SQLAlchemyBase


class BaseUser(SQLAlchemyBase):
  __tablename__ = 'users'
  __table_args__ = {**SQLAlchemyBase.__table_args__, **{'extend_existing': True}}

  public_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
  firebase_messaging_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

  @classmethod
  def getByPublicId(cls, dbSession, publicId: str, *entities):
    return dbSession \
      .query(*entities) \
      .filter(BaseUser.public_id == publicId) \
      .one_or_none()


class AppErrorLog(SQLAlchemyBase):
  __tablename__ = 'app_error_logs'

  tag: Mapped[str] = mapped_column(String(255), nullable=False)
  ip: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
  # -- Données en provenance du client
  http_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  http_method: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
  http_headers: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
  http_body: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
  # -- Données locales
  handler_name: Mapped[Optional[str]] = mapped_column(String(75), nullable=True)
  exception_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
  traceback: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
  user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))


class NotificationLog(SQLAlchemyBase):
  __tablename__ = 'notifications_logs'

  user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
  notification_type: Mapped[str] = mapped_column(SmallInteger(), nullable=False)
  token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  payload: Mapped[str] = mapped_column(Text(), nullable=False)
