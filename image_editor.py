from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from logger import logger
from os import getenv 

def edit_image(image: BytesIO, text: list) -> BytesIO:
  try:
    img = Image.open(image)
  except Exception as e:
    logger.error(f"An exception was thrown {e}")

  I1 = ImageDraw.Draw(img)

  width, height = img.size
  target_width = width * 0.9

  fontpath = f'{getenv("FONTPATH", "/usr/share/fonts/TTF/")}Impact.TTF'
  impact = []

  font_size = int(height * 0.35)
  for i in range(0,2):
    impact.append(ImageFont.truetype(fontpath, font_size))
    bbox = I1.textbbox((0, 0), text[i], font=impact[i])
    text_width = bbox[2] - bbox[0]
    counter = 0

    while text_width > target_width and font_size > 1 and counter < 1000:
        font_size -= 1
        impact[i] = ImageFont.truetype(fontpath, font_size)
        bbox = I1.textbbox((0, 0), text[i], font=impact[i])
        text_width = bbox[2] - bbox[0]
        counter += 1

        if font_size == 1:
          logger.info("Unable to minimize text enough")

  I1.text((width * 0.5, height * 0.1), text[0], font=impact[0], fill='white', stroke_width=3, stroke_fill='black', anchor='mm')
  I1.text((width * 0.5, height * 0.9), text[1], font=impact[1], fill='white', stroke_width=3, stroke_fill='black', anchor='mm')

  resulting_image = BytesIO()
  img.save(resulting_image, format="PNG")

  resulting_image.seek(0)
  return resulting_image
