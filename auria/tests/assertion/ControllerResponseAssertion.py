from abc import ABC
from typing import Optional, Dict

from flask import Response

from auria.Lang import Lang
from auria.Constants import BaseConstants


class ControllerResponseAssertion(ABC):

  @staticmethod
  def HTTPSuccess(response: Response, responseLength=0):
    assert response.status_code == 200
    assert response.json['success'] is True
    assert len(response.json) == responseLength + 1  # On ajoute le success = True

  @staticmethod
  def HTTPError(response: Response, errorCode: int, errorData: Optional[Dict] = None, language: str = BaseConstants.DEFAULT_LANGUAGE):
    assert response.status_code == 200
    assert response.json['success'] is False
    assert len(response.json) == 2

    # Error
    error = response.json['error']
    assert len(error) == 3
    assert error['code'] == errorCode
    assert error['message'] == Lang.getText(language, 'error_' + str(errorCode))
    assert error['data'] == errorData

  @staticmethod
  def HTTPAuthError(response: Response, error: str):
    assert response.status_code == 401
    assert response.get_data(as_text=True) == error
