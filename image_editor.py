from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from parser import get_random_image
from parser import get_random_text
from parser import send_image

def edit_image():
  get_random_image()
  top_header = get_random_text()
  bottom_header = get_random_text()

  img = Image.open('funny_image.jpg')
  img = img.resize((1500,1000))

  I1 = ImageDraw.Draw(img)

  impact = ImageFont.truetype('Impact.ttf', 80)

  I1.text((750, 50), top_header, font=impact, fill='white', stroke_width=2, stroke_fill='black', anchor='mm')
  I1.text((750, 950), bottom_header, font=impact, fill='white', stroke_width=2, stroke_fill='black', anchor='mm')

  img.save("funny_image_edited.png")
  send_image("funny_image_edited.png")
