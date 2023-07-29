from auria.utils.RegexUtils import ValidationUtils


class TestPasswordRegex:

  def test_regex(self):
    # ---------------- Errors
    assert ValidationUtils.isPasswordValid(None) is False  # None
    assert ValidationUtils.isPasswordValid('') is False  # None
    assert ValidationUtils.isPasswordValid(' ') is False  # None
    assert ValidationUtils.isPasswordValid('Nidal12') is False  # Too short
    assert ValidationUtils.isPasswordValid('Nidal123Nidal123Nidal123Nidal123N') is False  # Too long
    # assert ValidationUtils.isPasswordValid('nidal1234') is False  # Manque une majuscule
    # assert ValidationUtils.isPasswordValid('NIDAL1234') is False  # Manque une minuscule
    # assert ValidationUtils.isPasswordValid('NidalNidal') is False  # Manque un chiffre

    # ---------------- Success
    assert ValidationUtils.isPasswordValid('Nidal1234') is True
    assert ValidationUtils.isPasswordValid('RandomPassword89!') is True
    assert ValidationUtils.isPasswordValid('Random Password 89! ') is True


class TestNameRegex:

  def test_regex(self):
    # ---------------- Too short
    assert ValidationUtils.isNameValid(None) is False
    assert ValidationUtils.isNameValid('') is False
    assert ValidationUtils.isNameValid('  ') is False
    assert ValidationUtils.isNameValid('1') is False
    assert ValidationUtils.isNameValid('99') is False
    assert ValidationUtils.isNameValid('55 ') is False
    assert ValidationUtils.isNameValid(' Ni ') is False

    # ---------------- Number
    assert ValidationUtils.isNameValid('589') is False
    assert ValidationUtils.isNameValid('a97a') is False
    assert ValidationUtils.isNameValid('aa5') is False
    assert ValidationUtils.isNameValid('1sdqsd') is False
    assert ValidationUtils.isNameValid('1Npo') is False
    assert ValidationUtils.isNameValid('Nidal8') is False

    # ---------------- Special char
    assert ValidationUtils.isNameValid('Nidal<') is False
    assert ValidationUtils.isNameValid('Nidal>') is False
    assert ValidationUtils.isNameValid('Nidal{') is False
    assert ValidationUtils.isNameValid('Nidal}') is False
    assert ValidationUtils.isNameValid('Nidal"') is False
    assert ValidationUtils.isNameValid("Nidal\\") is False
    assert ValidationUtils.isNameValid('Nidal/') is False
    assert ValidationUtils.isNameValid('Nidal!') is False
    assert ValidationUtils.isNameValid('Nidal?') is False
    assert ValidationUtils.isNameValid('Nidal&') is False
    assert ValidationUtils.isNameValid('Nidal~') is False
    assert ValidationUtils.isNameValid('Nidal#') is False
    assert ValidationUtils.isNameValid('Nidal(') is False
    assert ValidationUtils.isNameValid('Nidal)') is False
    assert ValidationUtils.isNameValid('Nidal,') is False
    assert ValidationUtils.isNameValid('Nidal€') is False
    assert ValidationUtils.isNameValid('Nidal_') is False
    assert ValidationUtils.isNameValid('Nidal=') is False
    assert ValidationUtils.isNameValid('Nidal+') is False
    assert ValidationUtils.isNameValid('Nidal:') is False
    assert ValidationUtils.isNameValid('Nidal%') is False
    assert ValidationUtils.isNameValid('Nidal*') is False
    assert ValidationUtils.isNameValid('Nidal@') is False
    assert ValidationUtils.isNameValid('Nidal$') is False
    assert ValidationUtils.isNameValid('Nidal£') is False
    assert ValidationUtils.isNameValid('Nidal^') is False
    assert ValidationUtils.isNameValid('Nidal;') is False
    assert ValidationUtils.isNameValid('Nidal[') is False
    assert ValidationUtils.isNameValid('Nidal]') is False
    assert ValidationUtils.isNameValid('Nidal|') is False
    assert ValidationUtils.isNameValid('Nidal¿') is False
    assert ValidationUtils.isNameValid('Nidal§') is False
    assert ValidationUtils.isNameValid('Nidal«') is False
    assert ValidationUtils.isNameValid('Nidal»') is False
    assert ValidationUtils.isNameValid('Nidalω') is False
    assert ValidationUtils.isNameValid('Nidal⊙') is False
    assert ValidationUtils.isNameValid('Nidal¤') is False
    assert ValidationUtils.isNameValid('Nidal°') is False
    assert ValidationUtils.isNameValid('Nidal℃') is False
    assert ValidationUtils.isNameValid('Nidal℉') is False
    assert ValidationUtils.isNameValid('Nidal¥') is False
    assert ValidationUtils.isNameValid('Nidal¢') is False
    assert ValidationUtils.isNameValid('Nidal¡') is False
    assert ValidationUtils.isNameValid('Nidal©') is False
    assert ValidationUtils.isNameValid('Nidal®') is False

    # ---------------- Success
    assert ValidationUtils.isNameValid('Nidal\n') is True  # Le strip enleve le retour à la ligne
    assert ValidationUtils.isNameValid('Nidal') is True
    assert ValidationUtils.isNameValid('Nidal Nib') is True
    assert ValidationUtils.isNameValid('Nidal Nibça') is True
    assert ValidationUtils.isNameValid('Nidal Nibé') is True
    assert ValidationUtils.isNameValid('Nidal\'Nibé') is True
    assert ValidationUtils.isNameValid('Nidal \'Nibé') is True
    assert ValidationUtils.isNameValid('Nidal-Nibp') is True
    assert ValidationUtils.isNameValid('Nidal.D') is True
