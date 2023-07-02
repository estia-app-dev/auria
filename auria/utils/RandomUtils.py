import string
import uuid
from abc import ABC
from datetime import date
from random import choice, randint

from auria.utils.TextFormatUtils import TextFormatUtils


class RandomUtils(ABC):

  @staticmethod
  def uuid(removeDash: bool = False) -> str:
    generatedId = str(uuid.uuid4())
    return generatedId.replace("-", "") if removeDash else generatedId

  @staticmethod
  def generateString(size: int) -> str:
    return ''.join(choice(string.ascii_lowercase) for _ in range(size))

  @staticmethod
  def ageToRandomDate(age: int) -> str:
    today = date.today()
    year = today.year - age
    month = randint(1, today.month)
    month = TextFormatUtils.addZero(month)
    day = randint(1, 1)
    day = TextFormatUtils.addZero(day)

    return str(year) + '-' + month + '-' + day

  @staticmethod
  def fillStringWithRandomChars(txt: str, size: int):
    txtSize = len(txt)
    if txtSize == size:
      return txt
    return txt + '_' + RandomUtils.generateString(size=size - txtSize - 1)
