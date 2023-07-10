from firebase_admin.messaging import UnregisteredError
from sqlalchemy.orm import Session

from auria.Enums import AppErrorTagEnum
from auria.Exceptions import AppException
from auria.database.factories.AppErrorLogFactory import AppErrorLogFactory
from auria.database.factories.NotificationLogFactory import NotificationLogFactory
from auria.external_services.firebase.messaging.FCMMessage import FCMMessage
from auria.external_services.firebase.messaging.FirebaseMessagingApi import FirebaseMessagingApi


class Notification:

  def __init__(self, dbSession: Session, forTesting: bool = False):
    self.dbSession: Session = dbSession
    self.forTesting: bool = forTesting

  def send(self, message: FCMMessage):
    try:
      if message.token is None:
        raise AppException('FirebaseToken is empty')

      self.dbSession.add(NotificationLogFactory.create(message))
      FirebaseMessagingApi.send(message, forTesting=self.forTesting)

    except UnregisteredError:  # Le user à désinstallé l'app, osef on ne log pas
      pass
    except Exception as e:
      self._db_AddErrorLog(e, message)

  def _db_AddErrorLog(self, e, message: FCMMessage):
    appLog = AppErrorLogFactory.createExceptionLog(e, tag=AppErrorTagEnum.NOTIFICATION, user_id=message.userId, body=message.__dict__)
    self.dbSession.add(appLog)
