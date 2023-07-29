from abc import ABC, abstractmethod
from typing import Dict, Optional

from flask import request, jsonify
from sqlalchemy.orm import Session

from auria.Enums import MobilePlatformEnum
from auria.Env import Env
from auria.Exceptions import ApiAuthError, ApiException
from auria.api.ApiTokenManager import AppTokenManager, AppToken
from auria.ErrorCodes import ErrorCode
from auria.utils.ApiUtils import ApiUtils
from auria.utils.TraceUtils import TraceUtils


class Controller(ABC):

  def __init__(self, dbSession: Session):
    self.dbSession: Session = dbSession
    self.xPlatform = request.headers.get("x-platform", '0')
    self.xVersion = request.headers.get("x-version", None)
    self.json: Optional[Dict] = None

    if request.is_json:  # Content-Type: Application/json
      self.json = request.json

    # Headers obligatoires
    if self.xPlatform not in MobilePlatformEnum.toArray():
      raise ApiAuthError('Wrong x-platform header')
    if self.xVersion is None:
      raise ApiAuthError('Missing x-version header')
    if Env.getApiMinVersion() > float(self.xVersion):
      raise ApiException(ErrorCode.APP_NEED_TO_BE_UPDATED, 'RIP... raiseIF_apiVersionHasExpired')

  def HTTPResponse(self, data: Dict = None, debug: bool = False):
    data = {} if data is None else data
    data['success'] = True

    response = jsonify(data)

    if 'gzip' in request.headers.get('Accept-Encoding', ''):
      response = ApiUtils.compress(response)
      response.headers.add('Content-Encoding', 'gzip')

    response.headers.add('Content-Type', 'application/json; charset=utf-8')
    response.status_code = 200

    if debug:
      print('API response headers ->', TraceUtils.json_print(response.headers))
      print('API response will return ->', TraceUtils.json_print(data))

    return response

  @abstractmethod
  def handle(self, **kwargs):
    raise NotImplementedError


class BasicsAuthController(Controller, ABC):

  def __init__(self, dbSession: Session):
    super().__init__(dbSession)
    ApiUtils.checkBasicsAuth(Env.getApiBasicAuthUsername(), Env.getApiBasicAuthPassword())


class BearerTokenController(Controller, ABC):

  def __init__(self, dbSession: Session):
    super().__init__(dbSession)
    self.appToken: AppToken = AppToken().decode(self._decodeHeaderAppToken())

    if request.is_json:
      self.json['userId'] = self.userId

  @property
  def userId(self):
    return self.appToken.userId

  def _decodeHeaderAppToken(self) -> Dict:
    appToken = request.headers.get("x-appToken", None)

    if appToken is None:
      raise ApiAuthError('_decodeHeaderAppToken, appToken is missing')

    try:
      return AppTokenManager(secret=Env.getJWTSecret()).decode(appToken, verify=True)
    except Exception as e:
      if Env.inDevMode():
        raise
      raise ApiAuthError('_decodeHeaderAppToken, appToken is not recognized')
