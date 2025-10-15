import requests
import logging
from io import BytesIO
from random import randrange
from bs4 import BeautifulSoup
import os

base_url = "https://kasheloff.ru"
random_path = "/random"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive'
}

def get_random_image():
  try:
    random_response = requests.get(base_url + random_path, timeout=2, allow_redirects=True, headers=headers)
    random_response.raise_for_status()
    random_data = BeautifulSoup(random_response.text, 'html.parser')

    random_images = random_data.find_all('figure')
    if not random_images:
      raise ValueError("Не найдено элементов 'figure' на странице.")

    random_image_path = random_images[randrange(0, len(random_images))].find('a')['href']

    image_response = requests.get(base_url + random_image_path, timeout=2, headers=headers)
    image_response.raise_for_status()

    image_data = BeautifulSoup(image_response.text, 'html.parser')
    image_url = image_data.find('picture').find('img')['src']

    raw_image_response = requests.get(image_url, stream=True, timeout=10, headers=headers)
    raw_image_response.raise_for_status()

    image_bytes = BytesIO(raw_image_response.content)
    return image_bytes

  except requests.exceptions.RequestException as e:
    logger.error(f"An HTTP exception was thrown: {e}")
    return None
  except Exception as e:
    logger.error(f"An exception was thrown: {e}")
    return None
      
def get_random_text():
  try:
    random_text_list = []
    for i in range(2):
      random_response = requests.get(base_url + random_path, timeout=2, headers=headers)
      random_response.raise_for_status() 

      random_data = BeautifulSoup(random_response.text, 'html.parser')
      random_text = random_data.find('div', class_='post-title').find('h1').text
      random_text_list.append(random_text)

    return random_text_list

  except requests.exceptions.RequestException as e:
    logger.error(f"An HTTP exception was thrown: {e}")
    return None
  except Exception as e:
    logger.error(f"An exception was thrown: {e}")
    return None

def send_image(image_path):
  chat_id = os.getenv("CHAT_ID")
  bot_token = os.getenv("BOT_TOKEN")
  url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}'
  with open('funny_image_edited.png', 'rb') as image:
    print(requests.post(url, files={'photo': image}))

if __name__ == "__main__":
  logger.info(get_random_image())
  logger.info(get_random_text())
