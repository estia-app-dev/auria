from abc import ABC, abstractmethod
from typing import Optional, Dict

from flask import request, jsonify

from utils.ApiUtils import ApiUtils
from utils.TraceUtils import TraceUtils


class AuriaController(ABC):

  def __init__(self):
    self.json: Optional[Dict] = request.json if request.is_json else None

  def HTTPResponse(self, data: Dict = None, debug: bool = False):
    data = {} if data is None else data
    data['success'] = True

    response = jsonify(data)

    if 'gzip' in request.headers.get('Accept-Encoding', ''):
      response = ApiUtils.compress(response)
      response.headers.add('Content-Encoding', 'gzip')

    response.headers.add('Content-Type', 'application/json; charset=utf-8')
    response.status_code = 200

    if debug:
      print('API response headers ->', TraceUtils.json_print(response.headers))
      print('API response will return ->', TraceUtils.json_print(data))

    return response

  @abstractmethod
  def handle(self, **kwargs):
    raise NotImplementedError
