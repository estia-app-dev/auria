from typing import Dict, List


class FirebaseMessage:

  def __init__(self, token: str, body: str, data: Dict, forTesting=False):
    self.token = token
    self.body = body
    self.data = data
    self.forTesting = forTesting


class FirebaseMulticastMessage:

  def __init__(self, tokens: List[str], body: str, data: Dict, forTesting=False):
    self.tokens = tokens
    self.body = body
    self.data = data
    self.forTesting = forTesting
