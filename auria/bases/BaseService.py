from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from auria.Env import Env


class BaseService:

  @staticmethod
  def getDbEngine(timeout=5) -> Engine:
    return create_engine(
      url=Env.getDbServerURI(),
      echo=Env.isDbEcho(),
      connect_args={'connect_timeout': timeout}
    )

  @staticmethod
  def openDbSession() -> Session:
    session = sessionmaker(bind=BaseService.getDbEngine())
    return session()
