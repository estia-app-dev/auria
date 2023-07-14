from flask import Blueprint

from auria.api.ApiRouter import ApiRouter
from auria.tests.UnittestControllers import TempTestController, TempTestBearerController, TempTestBasicsAuthController

testApi = Blueprint('testApi', __name__)


@testApi.route('/test/exception/<int:exceptionId>', methods=['GET'])
def exceptionRoute(exceptionId: int):
  return ApiRouter.execute(TempTestController, exceptionId=exceptionId)


# Route pour tester la classe BasicsAuthController, voir TestApiController
@testApi.route('/test/basicsauth', methods=['GET'])
def basicsAuthRoute():
  return ApiRouter.execute(TempTestBasicsAuthController)


# Route pour tester la classe BearerTokenController, voir TestApiController
@testApi.route('/test/bearer', methods=['GET'])
def bearerRoute():
  return ApiRouter.execute(TempTestBearerController)
