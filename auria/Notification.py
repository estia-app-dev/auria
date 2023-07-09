from sqlalchemy.orm import Session

from auria.Enums import AppErrorTagEnum
from auria.Env import Env
from auria.database.factories.AppErrorLogFactory import AppErrorLogFactory
from auria.database.factories.NotificationLogFactory import NotificationLogFactory
from auria.external_services.firebase.messaging.FCMMessage import FCMMessage
from auria.external_services.firebase.messaging.FirebaseMessagingApi import FirebaseMessagingApi


class Notification:

  def __init__(self, dbSession: Session, forTesting: bool = False):
    self.dbSession: Session = dbSession
    self.forTesting: bool = forTesting

  def send(self, message: FCMMessage):
    if message.token is None:
      self.db_AddNotificationLog(message)
      pass

    # On log la notification
    self.db_AddNotificationLog(message)

    # On envoi la notification
    try:
      FirebaseMessagingApi.send(message, forTesting=self.forTesting)
    except BaseException:
      if Env.inDevMode():
        raise
      self.db_AddErrorLog(e)

  def db_AddNotificationLog(self, message: FCMMessage):
    try:
      notificationLog = NotificationLogFactory.create(message)
      self.dbSession.add(notificationLog)
    except BaseException:
      if Env.inDevMode():
        raise

  def db_AddErrorLog(self, e):
    try:
      AppErrorLogFactory.createExceptionLog(e, tag=AppErrorTagEnum.NOTIFICATION)
    except BaseException as e:
      if Env.inDevMode():
        raise e
