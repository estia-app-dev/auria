import base64
from abc import ABC

from auria.Env import Env


class UnittestData(ABC):

  @staticmethod
  def getBasicAuth() -> str:
    username = Env.getApiBasicAuthUsername()
    password = Env.getApiBasicAuthPassword()
    return 'Basic ' + base64.b64encode(bytes(username + ':' + password, 'ascii')).decode('ascii')
