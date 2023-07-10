from typing import Dict

from auria.Env import Env
from auria.misc.AesEncryption import AesEncryption


class BaseAppToken:
  USER_ID = 'email'

  def __init__(self, decodedToken: Dict, aesKey: str):
    aes = AesEncryption(aesKey)
    self.userId: str = aes.decode(decodedToken[BaseAppToken.USER_ID])
