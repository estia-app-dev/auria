import os
from abc import ABC

from auria.Enums import DevEnvironmentEnum
from auria.Exceptions import AppException
from auria.utils.TextFormatUtils import TextFormatUtils
from auria.utils.TraceUtils import TraceUtils


class Env(ABC):
  AVAILABLE_LANGUAGES = {}
  REQUIRED_VARS = [
    'E_ENV',
    'E_DEBUG',
    'E_DB_HOST',
    'E_DB_USERNAME',
    'E_DB_PASSWORD',
    'E_DB_NAME',
    'E_DB_ECHO',
  ]

  @staticmethod
  def isEnvVarExists(envVar: str):
    if os.getenv(envVar) is None:
      raise AppException('Missing ' + envVar + ' env var')

  @staticmethod
  def checkEnvironmentVars():
    for envVar in Env.REQUIRED_VARS:
      Env.isEnvVarExists(envVar)

  @staticmethod
  def setAppVars(devEnv: DevEnvironmentEnum, debug: bool):
    os.environ['E_ENV'] = devEnv.value
    os.environ['E_DEBUG'] = str(debug)

  @staticmethod
  def setDbVars(host: str, dbName: str, dbUsername: str, dbPassword: str, echo: bool = False):
    os.environ['E_DB_ECHO'] = str(echo)
    os.environ['E_DB_HOST'] = host
    os.environ['E_DB_NAME'] = dbName
    os.environ['E_DB_USERNAME'] = dbUsername
    os.environ['E_DB_PASSWORD'] = dbPassword

  @staticmethod
  def upsertRequiredVar(key: str, value):
    if key not in Env.REQUIRED_VARS:
      Env.REQUIRED_VARS.append(key)
    os.environ[key] = value

  ######################
  # ENVIRONMENT
  ######################

  @staticmethod
  def getEnv() -> str:
    return os.getenv('E_ENV', None)

  @staticmethod
  def debug() -> bool:
    return TextFormatUtils.strToBool(os.getenv('E_DEBUG', False))

  ######################
  # DATABASE
  ######################

  @staticmethod
  def getDbHost() -> str:
    return os.getenv('E_DB_HOST')

  @staticmethod
  def getDbUserName() -> str:
    return os.getenv('E_DB_USERNAME')

  @staticmethod
  def getDbPassword() -> str:
    return os.getenv('E_DB_PASSWORD')

  @staticmethod
  def getDbName() -> str:
    return os.getenv('E_DB_NAME')

  @staticmethod
  def isDbEcho() -> bool:
    return TextFormatUtils.strToBool(os.getenv('E_DB_ECHO', False))

  @staticmethod
  def getDbServerURI() -> str:
    uri = 'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    return uri.format(db_username=Env.getDbUserName(),
                      db_password=Env.getDbPassword(),
                      db_host=Env.getDbHost(),
                      db_name=Env.getDbName())

  #######################################################
  #######################################################

  @staticmethod
  def inDevMode() -> bool:
    return Env.getEnv() == DevEnvironmentEnum.DEVELOPMENT.value

  @staticmethod
  def inProductionMode() -> bool:
    return Env.getEnv() == DevEnvironmentEnum.PRODUCTION.value

  @staticmethod
  def inTestMode() -> bool:  # Identique au mode production, mais avec des vars env locales
    return Env.getEnv() == DevEnvironmentEnum.TEST.value

  #######################################################
  #######################################################

  @staticmethod
  def trace(*args, sep=' ', end='\n', file=None):
    if Env.debug():
      TraceUtils.debug(*args, sep, end, file)
