import json
import traceback
from abc import ABC

from auria.Enums import AppErrorTagEnum
from auria.Exceptions import AppException
from auria.database.DefaultTables import AppErrorLog
from auria.utils.DateUtils import DateUtils
from auria.utils.RandomUtils import RandomUtils


class AppErrorLogFactory(ABC):

  @staticmethod
  def create(tag: AppErrorTagEnum, **kwargs) -> AppErrorLog:
    body = kwargs.pop('http_body', None)
    headers = kwargs.pop('http_headers', None)

    appLog: AppErrorLog = AppErrorLog()
    appLog.id = RandomUtils.uuid()
    appLog.timestamp = DateUtils.now()
    appLog.tag = tag.value

    appLog.user_id = kwargs.pop('user_id', None)
    appLog.ip = kwargs.pop('ip', None)
    appLog.http_url = kwargs.pop('http_url', None)
    appLog.http_method = kwargs.pop('http_method', None)
    appLog.http_headers = None if headers is None else json.dumps(headers)
    appLog.http_body = None if body is None else json.dumps(body)
    appLog.handler_name = kwargs.pop('handler_name', None)
    appLog.exception_name = kwargs.pop('exception_name', None)
    appLog.traceback = kwargs.pop('traceback', None)

    if kwargs:
      print('Parameters args ->', kwargs)
      raise AppException('AppErrorLog parameters are not consumed')
    return appLog

  @staticmethod
  def createExceptionLog(e, tag: AppErrorTagEnum, **kwargs) -> AppErrorLog:
    kwargs['exception'] = e.__class__.__name__
    kwargs['traceback'] = traceback.format_exc()

    return AppErrorLogFactory.create(tag=tag, **kwargs)

  @staticmethod
  def createApiLog(e, tag: AppErrorTagEnum, httpUrl: str, httpMethod: str, httpHeaders, httpBody, ip: str) -> AppErrorLog:
    kwargs = {
      'http_url': httpUrl,
      'http_method': httpMethod,
      'http_headers': httpHeaders,
      'http_body': httpBody,
      'ip': ip,
    }

    return AppErrorLogFactory.createExceptionLog(e=e, tag=tag, **kwargs)
