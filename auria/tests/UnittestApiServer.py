from auria.Env import Env
from auria.api.ApiRouter import ApiRouter
from auria.tests.UnittestRoutes import testApi

flaskTestApp = ApiRouter.createFlaskApp()
flaskTestApp.register_blueprint(testApi, url_prefix='/')

flaskTestApp.config.update(
  ENV=Env.getEnv(),
  DEBUG=Env.debug(),
)

if __name__ == '__main__':
  flaskTestApp.run()
