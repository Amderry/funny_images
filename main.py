from parser import get_random_image_url, download_image, get_random_text
from sender import send_image
from image_editor import edit_image
from logger import logger

def main():
  try:
    text = get_random_text()
    logger.info(text)
    image = download_image()
    resulting_image = edit_image(image, text)
    logger.info(resulting_image)
    send_image(resulting_image)    
  except Exception as e:
    logger.error(f"An exception was thrown {e}")

if __name__ == "__main__":
  main()
