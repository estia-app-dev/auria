from enum import Enum, IntEnum


class DevEnvironment(Enum):
  DEVELOPMENT = 'development'
  PRODUCTION = 'production'
  TEST = 'test'


class TimeVal(IntEnum):
  ONE_MINUTE = 60
  ONE_HOUR = 3600
  ONE_DAY = 86400


class ExceptionLevel(Enum):
  INFO = 'I'
  ERROR = 'E'
  CRITICAL = 'C'  # Un cas qui se produit alors que normalement c'est impossible !!
