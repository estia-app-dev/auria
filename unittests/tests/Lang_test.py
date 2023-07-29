from auria.Lang import Lang
from auria.Constants import BaseConstants


class TestLang:
  DEFAULT = BaseConstants.DEFAULT_LANGUAGE.lower()

  def test_getText(self):
    assert Lang.getText(self.DEFAULT, 'unittest_en') == 'To be or not to be'  # Ok
    assert Lang.getText(self.DEFAULT, 'oops') == BaseConstants.DEFAULT_ERROR_MESSAGE  # Clé introuvable
    assert Lang.getText('fr', 'unittest_en') == 'To be or not to be'  # Le texte n'est pas traduit en FR
    assert Lang.getText(self.DEFAULT, 'unittest_fr') == BaseConstants.DEFAULT_ERROR_MESSAGE  # Clé introuvable
    assert Lang.getText('ca', 'unittest_en') == 'To be or not to be'  # Langue introuvable

  def test_getFormattedText(self):
    assert Lang.getFormattedText(self.DEFAULT, 'unittest_en_formatted', random='ohoho') == 'To be or not to be ohoho'
