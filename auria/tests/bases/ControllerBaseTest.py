import json
from abc import ABC, abstractmethod
from unittest.mock import patch

from flask import Response

from auria.Enums import MobilePlatformEnum
from auria.Env import Env
from auria.api.ApiTokenManager import AppTokenManager
from auria.tests.UnittestApiServer import flaskTestApp
from auria.tests.UnittestData import UnittestData
from auria.tests.bases.BaseTest import BaseTest
from auria.utils.TraceUtils import TraceUtils


class ControllerBaseTest(BaseTest, ABC):
  PATH = None
  METHOD = None

  @abstractmethod
  def test_EXPECTED_SCENARIO(self):
    raise NotImplementedError

  @property
  def client(self):
    return flaskTestApp.test_client()

  # On garde la méthode pure, l'ajout de données doit se faire dans les controllers enfants
  def fetch(self, **kwargs):
    headers = kwargs.pop('headers', {})

    if self.METHOD.upper() not in ['GET', 'DELETE'] and headers.get('Content-Length') != 0:
      headers['Content-Type'] = headers.get('Content-Type', 'application/json')

    path = kwargs.pop('path', self.PATH)  # Le path peut-etre custom dans le cas d'une URL avec un paramètre

    # multipart/form-data
    if 'form' in kwargs:
      kwargs['data'] = kwargs.pop('form')
    else:
      kwargs['data'] = json.dumps(kwargs.pop('data', None))

    kwargs['headers'] = headers

    if Env.debug():
      print('\n')
      print('API_TEST route ->', self.METHOD, path)
      print('API_TEST request headers ->', TraceUtils.json_print(kwargs['headers']))
      print('API_TEST request body ->', TraceUtils.json_print(kwargs.get('data', None)))

    response = self.client.open(path=path, method=self.METHOD, **kwargs)

    # Debug
    if Env.debug():
      print('API_TEST response ->', TraceUtils.json_print(response))

    return response


class BasicAuthControllerBaseTest(ControllerBaseTest, ABC):

  def prepareAuthorization(self) -> str:
    return UnittestData.getBasicAuth()

  def fetch(self, **kwargs) -> Response:
    headers = {
      'x-platform': kwargs.pop('xplatform', MobilePlatformEnum.APPLE),
      'x-version': kwargs.pop('xversion', Env.getApiMinVersion()),
      'Authorization': kwargs.pop('Authorization', UnittestData.getBasicAuth())
    }

    if 'headers' in kwargs:  # Merge des headers
      headers = {**headers, **kwargs.pop('headers')}

    self.dbSession.commit()  # On commit pour sync nos 2 sessions (Session ApiRoute + self.dbSession)
    return super().fetch(headers=headers, **kwargs)


class BearerControllerBaseTest(ControllerBaseTest, ABC):

  @patch('estia.api.controllers.Controller.BearerTokenController.raiseIF_bearerTokenIsInvalid')
  def fetch(self, mock, **kwargs) -> Response:
    headers = {
      'x-platform': kwargs.pop('x_platform', MobilePlatformEnum.APPLE),
      'x-version': kwargs.pop('x_version', Env.getApiMinVersion()),
      'Authorization': 'bearer '
    }

    if 'headers' in kwargs:  # Merge des headers
      headers = {**headers, **kwargs.pop('headers')}

    self.dbSession.commit()  # On commit pour sync nos 2 sessions (Session ApiRoute + self.dbSession)
    return super().fetch(headers=headers, **kwargs)
