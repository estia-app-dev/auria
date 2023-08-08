from abc import ABC
from typing import Union, List, Dict

from auria.Constants import Constants
from auria.Env import Env
from auria.Exceptions import AppException


class Lang(ABC):
  @staticmethod
  def getText(language: str, key: str, silent: bool = True) -> Union[str, List, Dict]:
    dataTxT = Env.AVAILABLE_LANGUAGES.get(language)

    try:
      # La clé existe dans la langue courante
      if key in dataTxT:
        return dataTxT[key]

      # La clé est introuvable dans la langue demandée, on va chercher la traduction dans le fichier de lang par défaut
      dataTxT = Env.AVAILABLE_LANGUAGES[Constants.DEFAULT_LANGUAGE]
      if key in dataTxT:
        return dataTxT[key]

      # Clé trouvable nulle part
      raise KeyError()

    except KeyError:
      if not silent:
        raise AppException('Message key not found -> ' + key)
      # On a pas traduit, on renvoi un message d'erreur
      return Constants.DEFAULT_ERROR_MESSAGE

  @staticmethod
  def getFormattedText(language: str, key: str, **kwargs):
    return Lang.getText(language, key).format(**kwargs)
