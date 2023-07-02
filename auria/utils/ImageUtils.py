import base64
from abc import ABC

from PIL import Image, ImageFilter


class ImageUtils(ABC):

  @staticmethod
  def toBase64(path):
    with open(path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  @staticmethod
  def resize(self, img, height: int, width: int, name: str, blur: bool):
    img.thumbnail((height, width), Image.ANTIALIAS)
    image_format = img.format.lower()

    if blur:
      img = img.filter(ImageFilter.GaussianBlur(5))
    img.save(self.savePath + name)

    return img, image_format

  @staticmethod
  def extractFormatFromName(imageName: str) -> str:
    return imageName.split('.')[1]
