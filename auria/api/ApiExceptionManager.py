import traceback

from flask import Response, jsonify

from auria.Enums import ExceptionLevelEnum
from auria.Env import Env
from auria.Exceptions import ApiException, AppException, JsonSchemaException, ApiAuthError
from auria.Lang import Lang
from auria.utils.ApiUtils import ApiUtils
from auria.utils.TraceUtils import TraceUtils


class ApiExceptionManager:
  """
  Execeptions gérées:
    -> ApiAuthError
    -> ApiException
    -> AppException
    -> JsonSchemaException
    -> Exception et autres ...
  """

  @staticmethod
  def addErrorHandlers(app):
    # Gestion des exceptions

    @app.errorhandler(ApiAuthError)
    def AuthErrorHandler(e: ApiAuthError):
      TraceUtils.debug('AuthError has been raised ->', e.message)  # En mode debug on affiche un message clair

      response = Response(e.message) if Env.inTestMode() else Response()
      response.headers.add('Content-Type', 'text/plain; charset=utf-8')
      response.status_code = 401
      return response

    @app.errorhandler(ApiException)
    def ApiExceptionHandler(e: ApiException):
      response: Response = jsonify({
        'success': False,
        'error': {
          'code': e.code,
          'message': Lang.getText(language=ApiUtils.getHeaderLanguage(), key='error_' + str(e.code)),
          'data': e.data,
        }
      })

      response.headers.add('Content-Type', 'application/json; charset=utf-8')
      response.status_code = 200
      return response

    @app.errorhandler(AppException)
    def AppExceptionHandler(e: AppException):
      if e.level == ExceptionLevelEnum.INFO:  # Rien de grave
        response: Response = jsonify({
          'success': True
        })
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 200
        return response
      else:
        return ExceptionHandler(e)

    @app.errorhandler(JsonSchemaException)
    def JsonSchemaExceptionHandler(e: JsonSchemaException):
      if Env.inDevMode():  # En mode dev, on affiche une réponse clair
        response: Response = jsonify({
          'message': e.message,
          'errors': [err.message for err in e.errors]
        })
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 500
        return response
      else:
        return ExceptionHandler(e)  # Y'a un truc mal codé coté client, ça reste une erreur grave

    @app.errorhandler(Exception)
    def ExceptionHandler(e):
      if Env.inDevMode():
        raise e

      if Env.debug():
        print(e)  # En mode debug on affiche un message clair
        print(traceback.format_exc())

      response: Response = Response('Ooooops something went wrong :(')
      response.headers.add('Content-Type', 'text/plain; charset=utf-8')
      response.status_code = 500
      return response
