from time import sleep

from flask import request, Blueprint, Flask

from auria.Enums import AppErrorTagEnum, ExceptionLevelEnum
from auria.Env import Env
from auria.Exceptions import ApiException, JsonSchemaException, AppException, ApiAuthError
from auria.bases.ServiceProviderBase import ServiceProvider
from auria.api.ApiExceptionManager import ApiExceptionManager

from auria.database.SQLAlchemyDatabase import dbSessionScope
from auria.database.factories.AppErrorLogFactory import AppErrorLogFactory
from auria.utils.ApiUtils import ApiUtils
from auria.utils.TraceUtils import TraceUtils

indexApi = Blueprint('indexApi', __name__)
tokenApi = Blueprint('tokenApi', __name__)
userApi = Blueprint('userApi', __name__)
# --
adminApi = Blueprint('adminApi', __name__)


class ApiRouter:

  @staticmethod
  def createFlaskApp() -> Flask:
    app = Flask(__name__)
    ApiExceptionManager.addErrorHandlers(app)

    return app

  @staticmethod
  def execute(func, **kwargs):
    if Env.inDevMode():
      # Dodo pour tester si besoin
      if 'sleep' in kwargs:
        sleep(kwargs.pop('sleep'))

      if Env.debug():
        print('Api request headers ->', TraceUtils.json_print(ApiUtils.getHeaders()))
        if request.is_json:
          print('Api Request ->', TraceUtils.json_print(request.json))

    # On enveloppe avec la connexion à la db
    with dbSessionScope(ServiceProvider.openDbSession()) as dbSession:
      try:
        return func(dbSession).handle(**kwargs)
      except (ApiException, ApiAuthError):
        raise  # On ne veux pas de log, on laisse la class ApiExceptionManager gérer le retour
      except(JsonSchemaException, AppException, Exception) as e:
        if isinstance(e, AppException):
          if e.level == ExceptionLevelEnum.INFO:
            raise  # On ne veux pas de log, on laisse la class Api gérer le retour

        # On annule tout
        dbSession.rollback()

        # On log + COMMIT
        errorLog = AppErrorLogFactory.createApiLog(e,
                                                   tag=AppErrorTagEnum.API_ERROR,
                                                   ip=request.remote_addr,
                                                   httpUrl=request.url,
                                                   httpMethod=request.method,
                                                   httpHeaders=ApiUtils.getHeaders(),
                                                   httpBody=request.get_json(silent=True))
        dbSession.add(errorLog)
        dbSession.commit()

        if Env.debug():
          TraceUtils.debug('-------------', 'New log généré depuis les routes d\'api')
          TraceUtils.debug(errorLog.__dict__)

        # On lève l'exception et on laisse la class ApiExceptionManager gérer le retour
        raise
