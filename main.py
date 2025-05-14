from image_editor import edit_image
from time import sleep

def main():
  edit_image()

if __name__ == "__main__":
  while True:
    try:
      main()
      sleep(1800)
    except Exception as e:
      print(e)
      continue
