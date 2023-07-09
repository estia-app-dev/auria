from abc import ABC
from typing import Union, Dict, List

from sqlalchemy.orm import Session

from auria.Enums import AppErrorTagEnum
from auria.Env import Env
from auria.database.DefaultTables import AppErrorLog
from auria.database.factories.AppErrorLogFactory import AppErrorLogFactory


class HandlerLogger(ABC):

  def __init__(self, dbSession: Session, className: str, body: Union[Dict, List]):
    self.dbSession: Session = dbSession
    self.className: str = className
    self.body = body
    self.tag = AppErrorTagEnum.HANDLER_ERROR

  def addLog(self, obj: Union[BaseException, AppErrorLog], silent: bool = False):
    """
    On ne souhaite pas qu'un log fasse planter le fonctionnement des handler.
    """
    try:
      if silent:
        self._db_addAppErrorLog(obj)
        return

      self.dbSession.rollback()  # On rollback() la merde qui a fait planter le script

      # On fournis l'objet log en param, pas besoin de le créér, on l'add
      if isinstance(obj, AppErrorLog):
        self.dbSession.add(obj)
        self.dbSession.commit()
      # Si c'est une exception, on créé le log
      elif isinstance(obj, BaseException):
        self._db_addAppErrorLog(obj)
        self.dbSession.commit()
      else:
        print('Obj type not found')
        return
    except Exception:
      if Env.inDevMode():
        raise

  def _db_addAppErrorLog(self, e: BaseException):
    appLog: AppErrorLog = AppErrorLogFactory.createExceptionLog(e, self.tag, body=self.body, handler=self.className)
    self.dbSession.add(appLog)
