import requests
from io import BytesIO
from os import getenv
from logger import logger
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_exponential

@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(1, 5),
    reraise=True 
)
def send_image(image: BytesIO):
  chat_id = getenv("CHAT_ID")
  bot_token = getenv("BOT_TOKEN")

  files = {
    'photo': ("image.png", image)
  }

  url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}'
  response = requests.post(url, files=files, timeout=5)
  response.raise_for_status()
