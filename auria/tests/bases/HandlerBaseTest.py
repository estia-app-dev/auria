from abc import ABC, abstractmethod
from typing import Union, Dict, List

from auria.ServiceProvider import BaseService
from auria.database.SQLAlchemyDatabase import dbSessionScope
from auria.tests.assertion.ExceptionRaisedAssertion import raise_JsonSchemaException
from auria.tests.bases.BaseTest import BaseTest


class HandlerBaseTest(BaseTest, ABC):
  SCHEMA_ERRORS = 0
  HANDLER = None

  @abstractmethod
  def test_EXPECTED_SCENARIO(self):
    raise NotImplementedError

  def execute(self, json: Union[Dict, List]):
    if self.HANDLER is None:
      raise ValueError('U have to set HANDLER var')

    with dbSessionScope(BaseService.openDbSession()) as dbSession:  # auto commit
      try:
        return self.HANDLER(dbSession, json).execute()
      finally:
        # Si le handler fais proc une exception, la connexion ne se ferme pas d'ou le try / finnaly
        self.dbSession.close()  # Force nos data à se refresh mais nécessite un second appel

  """
  TESTS
  """

  def test_JSON_SCHEMA_REQUIRED_PROPERTIES(self):
    if self.SCHEMA_ERRORS == 0:
      raise ValueError('U have to set SCHEMA_ERRORS var')

    @raise_JsonSchemaException(self.SCHEMA_ERRORS)
    def runTest():
      self.execute({})

    runTest()
