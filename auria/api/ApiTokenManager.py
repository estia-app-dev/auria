from typing import Dict

import jwt

from auria.utils.DateUtils import DateUtils
from auria.utils.RandomUtils import RandomUtils


class AppTokenManager:

  def __init__(self, secret: str):
    self.secret = secret
    self.algorithm = 'HS256'

  def encode(self, payload):
    return jwt.encode(key=self.secret, algorithm=self.algorithm, payload=payload)

  def decode(self, appToken: str, verify: bool = True) -> Dict:
    return jwt.decode(appToken, key=self.secret, algorithms=self.algorithm, verify=verify)

  def generateJWT(self, tokenData: Dict, appName='auria') -> str:
    token = {
      'id': RandomUtils.uuid(),  # Ne sert à rien, juste pour embrouiller celui qui lit le jwt
      'iss': appName,  # Le jeton est délivrée par l’application Estia
      'iat': DateUtils.now(),  # Le timestamp à partir duquel le jeton a été émis
    }

    return self.encode(token.update(tokenData))
