from typing import Optional, Dict, List

from sqlalchemy import String, ForeignKey, SmallInteger, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from auria.database.SQLAlchemyDatabase import SQLAlchemyBase


class BaseUser(SQLAlchemyBase):
  __tablename__ = 'users'
  __table_args__ = {**SQLAlchemyBase.__table_args__, **{'extend_existing': True}}

  public_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
  firebase_messaging_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  last_connexion_date = mapped_column(Integer(), nullable=False)
  #
  suspended_reason = mapped_column(SmallInteger(), nullable=False)
  suspended_date = mapped_column(Integer(), nullable=False)
  suspended_expiration_date = mapped_column(Integer(), nullable=False)
  #
  deleted_status = mapped_column(SmallInteger(), nullable=False)  # UserAccountDeletedStatusEnum
  deleted_retraction_date = mapped_column(Integer(), nullable=False)
  deleted_date = mapped_column(Integer(), nullable=False)

  @classmethod
  def getByPublicId(cls, dbSession, publicId: str, *entities):
    return dbSession \
      .query(*entities) \
      .filter(BaseUser.public_id == publicId) \
      .one_or_none()


class AppErrorLog(SQLAlchemyBase):
  __tablename__ = 'app_error_logs'

  tag = mapped_column(SmallInteger(), nullable=False)
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


class Setting(SQLAlchemyBase):
  __tablename__ = 'settings'

  key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  value: Mapped[str] = mapped_column(String(255), nullable=False)
  description: Mapped[str] = mapped_column(String(255), nullable=False)

  @classmethod
  def get(cls, dbSession, key: str) -> str:
    setting = dbSession \
      .query(Setting.value) \
      .filter(Setting.key == key) \
      .one_or_none()

    if setting is None:
      raise Exception(key + ' setting key not found')
    return setting.value

  @classmethod
  def gets(cls, dbSession, keys: List[str]) -> Dict:
    results = dbSession \
      .query(Setting) \
      .filter(Setting.key.in_(keys)) \
      .all()

    if not results:
      raise Exception('Setting keys not found')

    return {r.key: r.value for r in results}

  @classmethod
  def getAll(cls, dbSession) -> Dict:
    results = dbSession \
      .query(Setting) \
      .all()
    return {r.key: r.value for r in results}

  @classmethod
  def set(cls, dbSession, key: str, value):
    dbSession \
      .query(Setting) \
      .filter(Setting.key == key) \
      .update({'value': value})
