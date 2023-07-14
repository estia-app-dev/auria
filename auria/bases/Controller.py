from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

from flask import request, jsonify
from sqlalchemy.orm import Session

from auria.Enums import MobilePlatformEnum
from auria.Env import Env
from auria.Exceptions import ApiAuthError, ApiException
from auria.api.ApiTokenManager import AppTokenManager
from auria.bases.BaseAppToken import BaseAppToken
from auria.bases.BaseErrorCodes import BaseErrorCode
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
      raise ApiException(BaseErrorCode.APP_NEED_TO_BE_UPDATED, 'RIP... raiseIF_apiVersionHasExpired')

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
    self.appToken: Union[BaseAppToken or None] = None

    # On ajoute à notre JSON le user ID, on sait que tout nos handler ont besoin de cette valeur
    # Dans le cas d'une méthode par GET ou DELETE, le user ID est ajouté manuellement dans le controller
    if request.is_json:
      self.json['userId'] = self.getUserId()

    self.raiseIF_appTokenIsInvalid()

  def getUserId(self):
    return self.appToken.userId

  # L'appToken est généré par nous, si il n'est pas valide, le user sera déconnecté
  def raiseIF_appTokenIsInvalid(self):
    appToken = request.headers.get("x-appToken", None)
    if appToken is None:
      raise ApiAuthError('raiseIF_appTokenIsInvalid, appToken is missing')

    try:
      self.appToken = AppTokenManager(secret=Env.getJWTSecret()).decode(appToken, verify=True)
    except Exception as e:
      if Env.inDevMode():
        raise
      raise ApiAuthError('raiseIF_appTokenIsInvalid, appToken is not recognized')
