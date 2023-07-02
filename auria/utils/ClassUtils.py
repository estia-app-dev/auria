import inspect
from abc import ABC
from typing import List


class ClassUtils(ABC):

  @staticmethod
  def getClassVarName(cls) -> List:
    return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]

  @staticmethod
  def executeAllMethodsInClass(obj, *args, **kwargs):
    for name in dir(obj):
      attribute = getattr(obj, name)
      if inspect.ismethod(attribute):
        attribute(*args, **kwargs)

  @staticmethod
  def _setAttr(obj, **kwargs):
    for attr, value in kwargs.items():
      setattr(obj, attr, value)
