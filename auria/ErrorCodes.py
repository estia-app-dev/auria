from abc import ABC


class ErrorCode(ABC):
  INTERNAL_ERROR = -32
  APP_NEED_TO_BE_UPDATED = -33
