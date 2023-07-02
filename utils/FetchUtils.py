from abc import ABC
import time

import requests
from requests import Response, RequestException


class FetchUtils(ABC):

  @staticmethod
  def retryingFetch(url: str, timeout: int = 0, maxAttempts: int = 1, retryDelay: int = 1, **kwargs) -> Response:
    attempts = 1

    while True:
      try:
        if timeout == 0:
          r = requests.get(url, **kwargs)
        else:
          r = requests.get(url, timeout=timeout, **kwargs)

        r.raise_for_status()
        return r
      except RequestException as e:
        if attempts < maxAttempts:
          attempts += 1
          if retryDelay > 0:
            time.sleep(retryDelay)
          continue
        else:
          raise e
