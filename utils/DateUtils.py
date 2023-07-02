import calendar
import datetime
import time
from abc import ABC
from datetime import date


class DateFormat(ABC):
  FORMAT_YYYYMMDD = '%Y%m%d'
  FORMAT_YYYYMMDD_WITH_DASH = '%Y-%m-%d'
  FORMAT_YYYYMMDD_hhmmss_WITH_DASH = '%Y-%m-%d %H:%M:%S'
  FORMAT_YYYYMMDD_hhmmssff_WITH_DASH = '%Y-%m-%d %H:%M:%S.%f'
  FORMAT_DDMMYYYY_WITH_SLASH = '%d/%m/%Y'


class DateUtils(ABC):

  @staticmethod
  def now() -> int:
    return int(time.time())

  @staticmethod
  def midnight() -> int:
    return int(time.mktime(date.today().timetuple()))

  @staticmethod
  def toNight() -> int:
    tommorow = date.today() + datetime.timedelta(days=1)
    return int(time.mktime(tommorow.timetuple()) - 1)

  @staticmethod
  def currentStrDate(dateFormat: str = DateFormat.FORMAT_YYYYMMDD_WITH_DASH) -> str:
    return DateUtils.unixToStr(DateUtils.now(), dateFormat)

  @staticmethod
  def unixToStr(unixDate: int, dateFormat: str) -> str:
    if unixDate == 0:
      return ''
    return datetime.datetime.utcfromtimestamp(unixDate).strftime(dateFormat)

  @staticmethod
  def strToUnix(strDate: str, dateFormat: str) -> int:
    d = datetime.datetime.strptime(strDate, dateFormat)
    return calendar.timegm(d.utctimetuple())

  @staticmethod
  def formatDate(strDate: str, initialFormat: str, convertFormat: str) -> str:
    return datetime.datetime.strptime(strDate, initialFormat).strftime(convertFormat)

  @staticmethod
  def isUnixDateValid(unix: int) -> bool:
    try:
      strDate = DateUtils.unixToStr(unix, DateFormat.FORMAT_YYYYMMDD)
      int(datetime.datetime.strptime(strDate, DateFormat.FORMAT_YYYYMMDD).timestamp())
      return True
    except ValueError:
      return False

  @staticmethod
  def addDays(unix: int, days: int = 0, dateFormat: str = None):
    orig = datetime.datetime.fromtimestamp(unix)
    new = orig + datetime.timedelta(days=days)
    return int(new.timestamp()) if dateFormat is None else new.strftime(dateFormat)

  @staticmethod
  def addHours(unix: int, hours: int = 0, dateFormat: str = None):
    orig = datetime.datetime.fromtimestamp(unix)
    new = orig + datetime.timedelta(hours=hours)
    return int(new.timestamp()) if dateFormat is None else new.strftime(dateFormat)

  @staticmethod
  def addMinutes(unix: int, minutes: int = 0, dateFormat: str = None):
    orig = datetime.datetime.fromtimestamp(unix)
    new = orig + datetime.timedelta(minutes=minutes)
    return int(new.timestamp()) if dateFormat is None else new.strftime(dateFormat)

  @staticmethod
  def toHourMinutesSeconds(millis: int):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    return "%d hours %d minutes %d seconds" % (hours, minutes, seconds)

  @staticmethod
  def dateToAge(strDate: str):
    if isinstance(strDate, datetime.date):
      strDate = strDate.isoformat()

    today = date.today()
    yyyy, mm, dd = [int(x) for x in strDate.split('-')]
    age = today.year - yyyy - ((today.month, today.day) < (mm, dd))
    return age
