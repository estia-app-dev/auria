from abc import ABC

from requests import Session

from auria.tests.assertion.ControllerResponseAssertion import ControllerResponseAssertion
from auria.tests.assertion.UtilsAssertion import UtilsAssertion


class Assertion(ABC):

  def __init__(self, dbSession: Session):
    self._dbSession = dbSession
    self.controller = ControllerResponseAssertion
    self.utils = UtilsAssertion
