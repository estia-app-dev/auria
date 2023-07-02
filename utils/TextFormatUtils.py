from abc import ABC

from utils.DateUtils import DateFormat, DateUtils


class TextFormatUtils(ABC):

  @staticmethod
  def strToBool(val) -> bool:
    if type(val) == bool:
      return bool(val)
    if type(val) == int:
      return bool(val)
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1', 'True'):
      return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0', 'False'):
      return False
    else:
      raise ValueError("invalid truth value %r" % (val,))

  @staticmethod
  def addZero(value) -> str:
    return str(value) if value >= 10 else '0' + str(value)

  @staticmethod
  def formatBirthday(birthday: str) -> str:
    dateFormat = DateFormat.FORMAT_YYYYMMDD_WITH_DASH
    return DateUtils.formatDate(birthday, dateFormat, dateFormat)
