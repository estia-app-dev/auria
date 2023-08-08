from auria.Constants import Constants
from auria.Lang import Lang


class TestLang:
  DEFAULT = Constants.DEFAULT_LANGUAGE.lower()

  def test_getText(self):
    assert Lang.getText(self.DEFAULT, 'unittest_en') == 'To be or not to be'  # Ok
    assert Lang.getText(self.DEFAULT, 'oops') == Constants.DEFAULT_ERROR_MESSAGE  # Clé introuvable
    assert Lang.getText('fr', 'unittest_en') == 'To be or not to be'  # Le texte n'est pas traduit en FR
    assert Lang.getText(self.DEFAULT, 'unittest_fr') == Constants.DEFAULT_ERROR_MESSAGE  # Clé introuvable
    assert Lang.getText('ca', 'unittest_en') == 'To be or not to be'  # Langue introuvable

  def test_getFormattedText(self):
    assert Lang.getFormattedText(self.DEFAULT, 'unittest_en_formatted', random='ohoho') == 'To be or not to be ohoho'
