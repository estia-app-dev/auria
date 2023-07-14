from pytest import raises

from auria.Exceptions import JsonSchemaException, ApiException, AppException


def raise_AppException(exceptedMessage: str):
  def real_decorator(func):
    def wrapper(*args, **kwargs):
      with raises(AppException) as e:
        func(*args, **kwargs)
      assert exceptedMessage in str(e)

    return wrapper

  return real_decorator


def raise_JsonSchemaException(nbErrors: int):
  def real_decorator(func):
    def wrapper(*args, **kwargs):
      with raises(JsonSchemaException) as e:
        func(*args, **kwargs)
      assert len(e.value.errors) == nbErrors

    return wrapper

  return real_decorator


def raise_ApiException(errorCode: int):
  def real_decorator(func):
    def wrapper(*args, **kwargs):
      with raises(ApiException) as e:
        func(*args, **kwargs)
      assert e.value.code == errorCode

    return wrapper

  return real_decorator

