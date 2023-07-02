from typing import List, Optional, Dict

from AuriaEnums import ExceptionLevel


class AuriaBaseException(Exception):
  pass


class ValueException(AuriaBaseException):
  def __init__(self, code: int, message: str):
    self.code: int = code
    self.message: str = message


class AppException(AuriaBaseException):

  def __init__(self, message: str, level: ExceptionLevel = ExceptionLevel.ERROR):
    self.message: str = message
    self.level: ExceptionLevel = level


class JsonSchemaException(AuriaBaseException):

  def __init__(self, message: str, errors: List):
    self.message: str = message
    self.errors: List = errors
    super(Exception, self).__init__({"message": message, "errors": errors})


"""
Exceptions liées aux clients
"""


class ApiException(AuriaBaseException):
  """Exception à traiter coté client"""

  def __init__(self, code: int, message: str, data=None):
    self.code: int = code
    self.message: str = message
    self.data: Optional[Dict] = data


class ApiAuthError(AppException):
  """Erreur gérée côté client pour le basic ou le bearer"""
