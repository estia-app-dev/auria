from abc import ABC
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class SQLAlchemyDatabase:

  @staticmethod
  def createEngine(dburi: str, dbtimeout: int = 5, dbecho: bool = False) -> Engine:
    return create_engine(
      dburi,
      echo=dbecho,
      connect_args={'connect_timeout': dbtimeout}
    )


class DatabaseTable(ABC):
  MYSQL_ENGINE = 'InnoDB'
  MYSQL_COLLATE = 'utf8mb4_unicode_ci'

  __table_args__ = {
    'mysql_engine': MYSQL_ENGINE,
    'mysql_collate': MYSQL_COLLATE
  }


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
