import json
from abc import ABC

from auria.database.DefaultTables import NotificationLog
from auria.external_services.firebase.messaging.FCMMessage import FCMMessage
from auria.utils.DateUtils import DateUtils
from auria.utils.RandomUtils import RandomUtils


class NotificationLogFactory(ABC):

  @staticmethod
  def create(message: FCMMessage) -> NotificationLog:
    notificationLog: NotificationLog = NotificationLog()

    notificationLog.id = RandomUtils.uuid()
    notificationLog.timestamp = DateUtils.now()
    notificationLog.user_id = message.userId
    notificationLog.token = message.token
    notificationLog.notification_type = message.notificationType
    notificationLog.data = json.dumps(message.data)

    return notificationLog
