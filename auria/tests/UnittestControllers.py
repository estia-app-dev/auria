from sqlalchemy.orm import Session

from auria.Enums import ExceptionLevelEnum
from auria.Exceptions import ApiAuthError, JsonSchemaException, ApiException, AppException
from auria.ErrorCodes import BaseErrorCode
from auria.bases.ControllerBase import BasicsAuthController, BearerTokenController


# On créé un faux controller qui hérite de BasicsAuthController pour tester la class BasicsAuthController
# Voir TestApiController
class TempTestBasicsAuthController(BasicsAuthController):
  def handle(self, **kwargs):
    return self.HTTPResponse()


# On créé un faux controller qui hérite de BearerTokenController pour tester la class BearerTokenController
# Voir TestApiController
class TempTestBearerController(BearerTokenController):
  def handle(self, **kwargs):
    return self.HTTPResponse()


# On recréé une class controller, mais version light juste pour tester nos exceptions
class TempTestController:

  def __init__(self, dbSession: Session):
    self.dbSession: Session = dbSession
    self.json = None

  def handle(self, exceptionId: int):
    if exceptionId == 1:
      raise ApiAuthError('Wrong auth ids')
    if exceptionId == 2:
      raise JsonSchemaException('Wrong email', [])
    if exceptionId == 3:
      raise ApiException(BaseErrorCode.INTERNAL_ERROR, 'Internal error', data={'id': 5, 'token': 'myToken'})
    if exceptionId == 4:
      raise AppException('Ooopsi...')
    if exceptionId == 5:
      raise AppException('You sucks', ExceptionLevelEnum.INFO)
    if exceptionId == 6:
      raise ValueError('Invalid value')
    raise Exception('Unknow exceptionId')
