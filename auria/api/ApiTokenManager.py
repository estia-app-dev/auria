from typing import Dict

import jwt

from auria.Env import Env
from auria.misc.AesEncryption import AesEncryption
from auria.utils.DateUtils import DateUtils
from auria.utils.RandomUtils import RandomUtils


class ApiToken:
  USER_ID = 'email'
  SERVER_TOKEN = 'password'

  def __init__(self):
    self.aes = AesEncryption(Env.getServerAesKey())
    self.userId: str = ''
    self.serverToken: str = ''

  def encode(self, userId: str):
    self.userId: str = self.aes.encode(userId)
    self.serverToken: str = Env.getServerToken()

  def decode(self, decodedToken: Dict):
    self.userId: str = self.aes.decode(decodedToken[ApiToken.USER_ID])
    self.serverToken = decodedToken[ApiToken.SERVER_TOKEN]

  def toDict(self) -> Dict:
    return {
      ApiToken.USER_ID: self.userId,
      ApiToken.SERVER_TOKEN: self.serverToken
    }


class ApiTokenManager:

  def __init__(self, secret: str):
    self.secret = secret
    self.algorithm = 'HS256'

  def encode(self, payload):
    return jwt.encode(key=self.secret, algorithm=self.algorithm, payload=payload)

  def decode(self, strToken: str, verify: bool = True) -> Dict:
    return jwt.decode(strToken, key=self.secret, algorithms=self.algorithm, verify=verify)

  def generateJWT(self, apiToken: ApiToken, appName='auria') -> str:
    token = {
      'id': RandomUtils.uuid(),  # Ne sert à rien, juste pour embrouiller celui qui lit le jwt
      'iss': appName,  # Le jeton est délivrée par l’application
      'iat': DateUtils.now()  # Le timestamp à partir duquel le jeton a été émis
    }

    return self.encode(token.update(apiToken.toDict()))
