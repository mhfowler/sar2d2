import RPi.GPIO as GPIO
import time
import os
import json

from hello_settings import SECRETS_DICT
from pi_utilities.telegram_helper import telegram_log, send_telegram


def press_button():
  for i in range(0, 1):
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz

    p.start(2.5)  # Initialization
    try:
      p.ChangeDutyCycle(6.7)
      time.sleep(1.5)
      p.ChangeDutyCycle(2.5)
      time.sleep(0.5)
    finally:
      p.stop()
      GPIO.cleanup()
      time.sleep(0.5)


if __name__ == '__main__':
  time.sleep(2)
  try:
    r_file_path = SECRETS_DICT['REBOOT_LOG_FILE']
    if os.path.isfile(r_file_path):
      with open(r_file_path, 'r') as r_file:
        print('++ trying to load reboot_file {}'.format(r_file_path))
        data_dict = json.loads(r_file.read())
        t_id = data_dict['t_id']
        send_telegram(chat_id=t_id, msg='++ trying to open the door now')
        telegram_log('++ tried to open after reboot for {}'.format(t_id))
        os.remove(r_file_path)
  except:
    pass
  press_button()