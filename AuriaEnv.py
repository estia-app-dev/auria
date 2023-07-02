import os
from abc import ABC

from AuriaEnums import DevEnvironment
from AuriaException import AppException
from utils.TextFormatUtils import TextFormatUtils


class AuriaEnv(ABC):

  @staticmethod
  def isEnvironmentVarExists(envVar: str):
    if os.getenv(envVar) is None:
      raise AppException('Missing ' + envVar + ' env var')

  @staticmethod
  def checkAppVars():
    required_vars = [
      'E_ENV',
      'E_DEBUG',
      'E_DB_HOST',
      'E_DB_USERNAME',
      'E_DB_PASSWORD',
      'E_DB_NAME',
      'E_DB_ECHO',
    ]

    for envVar in required_vars:
      AuriaEnv.isEnvironmentVarExists(envVar)

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
    return uri.format(db_username=AuriaEnv.getDbUserName(),
                      db_password=AuriaEnv.getDbPassword(),
                      db_host=AuriaEnv.getDbHost(),
                      db_name=AuriaEnv.getDbName())

  #######################################################
  #######################################################

  @staticmethod
  def inDevMode() -> bool:
    return AuriaEnv.getEnv() == DevEnvironment.DEVELOPMENT.value

  @staticmethod
  def inProductionMode() -> bool:
    return AuriaEnv.getEnv() == DevEnvironment.PRODUCTION.value

  @staticmethod
  def inTestMode() -> bool:  # Identique au mode production, mais avec des vars env locales
    return AuriaEnv.getEnv() == DevEnvironment.TEST.value
