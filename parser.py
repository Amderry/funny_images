import requests
import shutil
from random import randrange
from bs4 import BeautifulSoup
import os

base_url = "https://kasheloff.ru"
random_path = "/random"

def get_random_image():
  random_response = requests.get(base_url + random_path, timeout=2).text
  random_data = BeautifulSoup(random_response, 'html.parser')
  random_images = random_data.find_all('figure')
  random_image_path = random_images[randrange(0, len(random_images))].find('a')['href']

  image_response = requests.get(base_url + random_image_path, timeout=2).text
  image_data = BeautifulSoup(image_response, 'html.parser')
  image_url = image_data.find('picture').find('img')['src']
  
  with open('funny_image.jpg', 'wb') as image:
    try:
      raw_image = requests.get(image_url, stream=True, timeout=2).raw
      shutil.copyfileobj(raw_image, image)
    except Exception as e:
      print("Exception occured: ", e)
      
def get_random_text():
  random_response = requests.get(base_url + random_path, timeout=2).text
  random_data = BeautifulSoup(random_response, 'html.parser')
  random_text = random_data.find('div', class_='post-title').find('h1').text
  return random_text

def send_image(image_path):
  chat_id = os.getenv("CHAT_ID")
  bot_token = os.getenv("BOT_TOKEN")
  url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}'
  print(url)
  with open('funny_image_edited.png', 'rb') as image:
    print(requests.post(url, files={'photo': image}))
