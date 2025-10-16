import requests
from curl_cffi import requests as cc_requests
from io import BytesIO
from random import randrange
from bs4 import BeautifulSoup
from logger import logger
from texts import texts
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_none
import os

base_url = "https://kasheloff.ru"
random_path = "/random"

headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive'
}

def get_random_image_url() -> str:
  try:
    random_response = cc_requests.get(base_url + random_path, timeout=2, allow_redirects=True, headers=headers, impersonate="chrome")
    random_response.raise_for_status()
    random_data = BeautifulSoup(random_response.text, 'html.parser')

    random_images = random_data.find_all('figure')
    if not random_images:
      raise ValueError("Не найдено элементов 'figure' на странице.")

    random_image_path = random_images[randrange(0, len(random_images))].find('a')['href']

    image_response = cc_requests.get(base_url + random_image_path, timeout=2, headers=headers, impersonate="chrome")
    image_response.raise_for_status()

    image_data = BeautifulSoup(image_response.text, 'html.parser')
    image_url = image_data.find('picture').find('img')['src']
    return image_url
    
  except requests.exceptions.RequestException as e:
    logger.error(f"An HTTP exception was thrown: {e}")
    return None
  except Exception as e:
    logger.error(f"An exception was thrown: {e}")
    return None
      
@retry(
    stop=stop_after_attempt(10), 
    wait=wait_none(),
    reraise=True 
)
def download_image() -> BytesIO:
  url = get_random_image_url()
  logger.info(url)
  raw_image_response = requests.get(url, stream=True, timeout=3, headers=headers)
  raw_image_response.raise_for_status()

  image_bytes = BytesIO(raw_image_response.content)
  return image_bytes

def get_random_text():
  try:
    random_text_list = []
    for i in range(2):
      if randrange(0, 100) > 2:
        random_response = cc_requests.get(base_url + random_path, timeout=2, headers=headers, impersonate="chrome")
        random_response.raise_for_status() 

        random_data = BeautifulSoup(random_response.text, 'html.parser')
        random_text = random_data.find('div', class_='post-title').find('h1').text
        random_text_list.append(random_text)
      else:
        random_text_list.append(texts[randrange(0, len(texts))])

    return random_text_list

  except requests.exceptions.RequestException as e:
    logger.error(f"An HTTP exception was thrown: {e}")
    return None
  except Exception as e:
    logger.error(f"An exception was thrown: {e}")
    return None
