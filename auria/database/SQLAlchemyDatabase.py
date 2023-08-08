from contextlib import contextmanager

from sqlalchemy import create_engine, String, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Get by Primary Key > https://docs.sqlalchemy.org/en/20/orm/session_basics.html#get-by-primary-key
# Expiring / Refreshing > https://docs.sqlalchemy.org/en/20/orm/session_basics.html#expiring-refreshing
class SQLAlchemyBase(DeclarativeBase):
  MYSQL_ENGINE = 'InnoDB'
  MYSQL_COLLATE = 'utf8mb4_unicode_ci'

  __table_args__ = {
    'mysql_engine': MYSQL_ENGINE,
    'mysql_collate': MYSQL_COLLATE
  }

  id: Mapped[str] = mapped_column(String(36), primary_key=True)
  timestamp = mapped_column(Integer(), nullable=False)


class SQLAlchemyDb:

  @staticmethod
  def createEngine(dburi: str, dbtimeout: int = 5, dbecho: bool = False) -> Engine:
    return create_engine(
      dburi,
      echo=dbecho,
      connect_args={'connect_timeout': dbtimeout}
    )

  @staticmethod
  def createDatabase(engine):
    metadata = SQLAlchemyBase.metadata
    metadata.create_all(engine)


@contextmanager
def dbSessionScope(session):
  try:
    yield session
    session.commit()
  except:
    session.rollback()
    raise
  finally:
    session.close()
