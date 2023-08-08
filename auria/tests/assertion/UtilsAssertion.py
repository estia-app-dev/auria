from abc import ABC

from auria.Constants import Constants
from auria.Lang import Lang
from auria.utils.DateUtils import DateUtils


class UtilsAssertion(ABC):

  @staticmethod
  def coordinates(c1, c2):
    assert round(float(c1), 4) == round(c2, 4)

  @staticmethod
  def unixDate(unixDate: int, delay: int = 0):
    # Il faut controler les date mise à jour lors du test. Controler une date ecite dans les datasets va planter à cause du decelage
    # Le -20 est une durée minimal, on considere qu'un test ne dure pas plus de 60s
    assert unixDate > 0
    assert unixDate >= DateUtils.now() + delay - 10
    assert unixDate <= DateUtils.now() + delay + 10

  @staticmethod
  def uuid(txt, size: int = 36):
    assert len(txt) == size

  @staticmethod
  def langText(txt: str, key: str, language: str):
    assert txt is not None
    assert txt != Constants.DEFAULT_ERROR_MESSAGE
    assert txt == Lang.getText(language, key)
