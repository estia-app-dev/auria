from typing import Dict, Optional


class FCMMessage:

  def __init__(self, userId: str, publicId: str, token: str):
    self.token: Optional[str] = token
    self.userId: str = userId
    self.publicId: str = publicId
    self.notificationType = -1
    self.text = None
    self.data = {}

  def setMessage(self, notificationType: int, text: str, data: Dict):
    self.notificationType = notificationType
    self.text = text
    self.data = data
