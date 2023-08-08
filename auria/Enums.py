from auria.misc.ExtendedEnum import ExtendedIntEnum


class DevEnvironmentEnum(ExtendedIntEnum):
  DEVELOPMENT = 4
  PRODUCTION = 6
  TEST = 8


class TimeValEnum(ExtendedIntEnum):
  ONE_MINUTE = 60
  ONE_HOUR = 3600
  ONE_DAY = 86400


class ExceptionLevelEnum(ExtendedIntEnum):
  INFO = 2
  ERROR = 5
  CRITICAL = 8  # Un cas qui se produit alors que normalement c'est impossible !!


class AppErrorTagEnum(ExtendedIntEnum):
  NOTIFICATION = 2
  AWS = 4
  API_ERROR = 6
  ADMIN_API_ERROR = 8
  HANDLER_ERROR = 10


class MobilePlatformEnum(ExtendedIntEnum):
  APPLE = 2
  GOOGLE = 3


class UserAccountDeletedStatusEnum(ExtendedIntEnum):
  WILL_BE_DELETED = 1
  HAS_BEEN_DELETED = 2


class GenderEnum(ExtendedIntEnum):
  MALE = 1
  FEMALE = 2

  def getOppositeGender(self) -> int:
    if self == GenderEnum.MALE.value:
      return GenderEnum.FEMALE.value
    if self == GenderEnum.FEMALE.value:
      return GenderEnum.MALE.value
    raise ValueError('Gender not found')
