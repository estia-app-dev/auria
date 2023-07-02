import gzip
import json
from abc import ABC
from typing import Dict, Union

from flask import request, Response, make_response

from auria.utils.RandomUtils import RandomUtils


class ApiUtils(ABC):

  @staticmethod
  def compress(data) -> Response:
    content = gzip.compress(json.dumps(data).encode('utf8'), 5)
    return make_response(content)

  @staticmethod
  def getHeaderLanguage(defaultLanguage: str = 'en'):
    return request.headers.get('Accept-Language', defaultLanguage)

  @staticmethod
  def getHeaders() -> Dict:
    headers: Dict = dict()
    for header in request.headers.__iter__():
      headers[header[0]] = header[1]
    return headers

  @staticmethod
  def getBearerToken() -> Union[str or None]:
    auth = request.headers.get("Authorization", None)
    if not auth:
      return None

    parts = auth.split()

    if parts[0].lower() != "bearer":
      return None
    elif len(parts) == 1:
      return None
    elif len(parts) > 2:
      return None

    return parts[1]

  # Todo à tester
  @staticmethod
  def getRemoteAddr():
    # Y'a un proxy entre flask et je sais pas quoi. Sans cette methode l'IP du user est toujours 127.0.0.1 (adress local du proxy)
    try:
      headers_list = request.headers.getlist("X-Forwarded-For")
      user_ip = headers_list[0] if headers_list else request.remote_addr
      if user_ip == '127.0.0.1':
        return RandomUtils.generateString(size=15)
      return user_ip
    except BaseException:
      return RandomUtils.generateString(size=15)

  @staticmethod
  def checkBasicsAuth(username, password):
    authorization = request.authorization
    if authorization is None:
      raise ValueError('Authorization header is not valid')

    areAuthValid = username == authorization.username and password == authorization.password

    if not authorization or not areAuthValid:
      raise ValueError('Authorization header is not valid')