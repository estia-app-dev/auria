from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from auria.bases.ServiceProvider import ServiceProvider


class BaseTest(ABC):
  dbSessionTemp: Session = None

  @property
  def dbSession(self):
    if BaseTest.dbSessionTemp is None:
      BaseTest.dbSessionTemp = ServiceProvider.openDbSession()
    return BaseTest.dbSessionTemp

  def teardown_method(self):  # Lorsque que le test se termine
    if BaseTest.dbSessionTemp is not None:
      BaseTest.dbSessionTemp.close()

  @abstractmethod
  def setup_method(self):  # Avant le test
    raise NotImplementedError

  @abstractmethod
  @property
  def assertion(self):  # Implementer une class qui hérite de BaseAssertion
    raise NotImplementedError

  @abstractmethod
  @property
  def dbData(self):
    raise NotImplementedError
