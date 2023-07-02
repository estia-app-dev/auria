import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AesEncryption:

  def __init__(self, key: str):
    self.key = key.encode("utf8")  # b'key

  def encode(self, raw: str):
    bRaw = raw.encode("utf8")

    cipher = AES.new(self.key, AES.MODE_CBC)  # L'iv est généré aleatoirement
    cipherData = cipher.encrypt(pad(bRaw, AES.block_size))
    return base64.b64encode(cipher.iv + cipherData).decode()

  def decode(self, encodedData):
    decoded = base64.b64decode(encodedData)

    iv = decoded[:AES.block_size]
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    dPadded = cipher.decrypt(decoded[AES.block_size:])

    return unpad(dPadded, AES.block_size).decode()
