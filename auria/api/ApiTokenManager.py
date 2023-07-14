from typing import Dict

import jwt

from auria.Env import Env
from auria.misc.AesEncryption import AesEncryption
from auria.utils.DateUtils import DateUtils
from auria.utils.RandomUtils import RandomUtils


class AppToken:
  USER_ID = 'email'
  SERVER_TOKEN = 'password'
  DEVICE_ID = 'pet'  # Detection de connexion sur de multiple devices

  def __init__(self):
    self.aes = AesEncryption(Env.getServerAesKey())
    self.userId: str = ''
    self.deviceId: str = ''
    self.serverToken: str = ''

  def encode(self, userId: str, deviceId: str):
    self.userId: str = self.aes.encode(userId)
    self.deviceId = deviceId
    self.serverToken: str = Env.getServerToken()

  def decode(self, decodedToken: Dict):
    self.userId: str = self.aes.decode(decodedToken[AppToken.USER_ID])
    self.deviceId = decodedToken[AppToken.DEVICE_ID]
    self.serverToken = decodedToken[AppToken.SERVER_TOKEN]

  def toDict(self) -> Dict:
    return {
      AppToken.USER_ID: self.userId,
      AppToken.DEVICE_ID: self.deviceId,
      AppToken.SERVER_TOKEN: Env.getServerToken()
    }


class AppTokenManager:  # Pas utilisé

  def __init__(self, secret: str):
    self.secret = secret
    self.algorithm = 'HS256'

  def encode(self, payload):
    return jwt.encode(key=self.secret, algorithm=self.algorithm, payload=payload)

  def decode(self, appToken: str, verify: bool = True) -> Dict:
    return jwt.decode(appToken, key=self.secret, algorithms=self.algorithm, verify=verify)

  def generateJWT(self, appToken: AppToken, appName='auria') -> str:
    token = {
      'id': RandomUtils.uuid(),  # Ne sert à rien, juste pour embrouiller celui qui lit le jwt
      'iss': appName,  # Le jeton est délivrée par l’application
      'iat': DateUtils.now()  # Le timestamp à partir duquel le jeton a été émis
    }

    return self.encode(token.update(appToken.toDict()))
