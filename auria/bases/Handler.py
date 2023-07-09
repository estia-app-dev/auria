from abc import ABC, abstractmethod
from typing import Union, Dict, List

from sqlalchemy.orm import Session

from auria.bases.HandlerLogger import HandlerLogger
from auria.misc.JsonSchemaValidator import JsonSchemaValidator
from auria.utils.DateUtils import DateUtils


class Handler(ABC):

  def __init__(self, dbSession: Session, body: Union[Dict, List]):
    self._raiseIf_JsonSchemaIsInvalid(body)

    if not isinstance(dbSession, Session):
      raise TypeError('DbSession must be type of Session')

    self.dbSession: Session = dbSession
    self.body: Union[Dict, List] = body
    self.now: int = DateUtils.now()
    self.logger = HandlerLogger(self.dbSession, className=self.__class__.__name__, body=body)

  def getAttribute(self, key: str, silent: bool = True):
    if key not in self.body and not silent:
      raise AttributeError(key + ', not found on json')
    return self.body.get(key)

  def _raiseIf_JsonSchemaIsInvalid(self, json):
    schema = self.defineSchema()
    if isinstance(schema, dict):
      JsonSchemaValidator(schema, json).validate()

  @abstractmethod
  def defineSchema(self):
    raise NotImplementedError()

  @abstractmethod
  def handle(self, **kwargs):
    raise NotImplementedError()
