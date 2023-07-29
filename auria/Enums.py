from enum import Enum, IntEnum

from auria.misc.ExtendedEnum import ExtendedIntEnum


class DevEnvironmentEnum(Enum):
  DEVELOPMENT = 'development'
  PRODUCTION = 'production'
  TEST = 'test'


class TimeValEnum(IntEnum):
  ONE_MINUTE = 60
  ONE_HOUR = 3600
  ONE_DAY = 86400


class ExceptionLevelEnum(Enum):
  INFO = 'I'
  ERROR = 'E'
  CRITICAL = 'C'  # Un cas qui se produit alors que normalement c'est impossible !!


class AppErrorTagEnum(Enum):
  NOTIFICATION = 'NOTIFICATION'
  AWS = 'AWS'
  API_ERROR = 'API_ERROR'
  ADMIN_API_ERROR = 'ADMIN_API_ERROR'
  HANDLER_ERROR = 'HANDLER_ERROR'


class MobilePlatformEnum(ExtendedIntEnum):
  APPLE = 2
  GOOGLE = 3
