import json
from abc import ABC
from datetime import datetime, date


class TraceUtils(ABC):

  @staticmethod
  def debug(*args, sep=' ', end='\n', file=None):
    try:
      print(*args, sep=sep, end=end, file=file)
    except Exception:
      pass

  @staticmethod
  def json_print(data):
    def jsonSerial(obj):
      """JSON serializer for objects not serializable by default json code"""
      if isinstance(obj, (datetime, date)):
        return obj.isoformat()
      raise TypeError("Type %s not serializable" % type(obj))

    try:
      return json.dumps(data, indent=4, sort_keys=False, default=jsonSerial)
    except TypeError:
      return data
