import re
from abc import ABC
from typing import Optional


class ValidationUtils(ABC):

  @staticmethod
  def isUrlValid(url: str) -> bool:
    if not isinstance(url, str):
      return False
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(url_pattern.match(url))

  @staticmethod
  def isMailValid(email: str) -> bool:
    if not isinstance(email, str) or len(email.strip()) == 0:
      return False
    email = email.strip()
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

  @staticmethod
  def isPasswordValid(password: Optional[str]) -> bool:
    if not isinstance(password, str):
      return False

    # At least one digit [0-9]
    # At least one lowercase character [a-z]
    # At least one uppercase character [A-Z]
    # At least 8 characters in length, but no more than 32.
    # pattern = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}$"
    pattern = r"^.{8,32}$"
    return re.match(pattern, password) is not None

  @staticmethod
  def isNameValid(name: Optional[str]) -> bool:
    if not isinstance(name, str) or len(name.strip()) == 0:
      return False

    name = name.strip()

    # Trop court
    if len(name) <= 2:
      return False
    # On vérifie si le nom contient des caratères spéciaux
    # \\\\  == Backslash
    # \/    == Slash
    if re.search(r"[0-9<>{}\"&\\~/!?#(),€_=:%*$£;+@^\[\]|¿§«»ω⊙¤°℃℉¥¢¡®©™¦¬¶]+", name) is not None:
      return False

    return True
