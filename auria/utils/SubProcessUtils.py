import subprocess
from abc import ABC
from typing import List


class SubProcessUtils(ABC):

  @staticmethod
  def executeAndWait(cmd: List):
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
    return p.communicate()  # return out, err = p.communicate()
