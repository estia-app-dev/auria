from abc import ABC, abstractmethod
from typing import Union, Dict, List

from sqlalchemy.orm import Session

from misc.JsonSchemaValidator import JsonSchemaValidator
from utils.DateUtils import DateUtils


class Handler(ABC):

  def __init__(self, dbSession: Session, json: Union[Dict, List], data: Dict = None):
    self.raiseIf_JsonSchemaIsInvalid(json)

    if not isinstance(dbSession, Session):
      raise TypeError('DbSession must be type of Session')

    self.dbSession: Session = dbSession
    self.json: Union[Dict, List] = json
    self.data: Dict = data
    self.now: int = DateUtils.now()

  def getAttribute(self, key: str, silent: bool = True):
    if key not in self.json and not silent:
      raise AttributeError(key + ', not found on json')
    return self.json.get(key)

  def raiseIf_JsonSchemaIsInvalid(self, json):
    schema = self.defineSchema()
    if isinstance(schema, dict):
      JsonSchemaValidator(schema, json).validate()

  @abstractmethod
  def defineSchema(self):
    raise NotImplementedError()

  @abstractmethod
  def handle(self, **kwargs):
    raise NotImplementedError()
