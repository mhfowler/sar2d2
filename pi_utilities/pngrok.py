import time
import re

from pyngrok import ngrok

from pi_utilities.telegram_helper import telegram_log
from hello_settings import SECRETS_DICT


ngrok_token = SECRETS_DICT['NGROK_TOKEN']


if __name__ == '__main__':
  # Open a tunnel on the default port 80
  ngrok.set_auth_token(ngrok_token)
  public_url = ngrok.connect(port=22, proto="tcp")

  regex = '^tcp:\/\/(\d+\.tcp\.ngrok\.io)\:(\d+?)$'
  match = re.match(regex, public_url)
  if match:
    ssh_string = 'ssh pi@{} -p{}'.format(match.group(1), match.group(2))
    telegram_log('ngrok is now connected: {}'.format(ssh_string))
  else:
    telegram_log('ngrok is now connected: {}'.format(public_url))


  while True:
    time.sleep(1)
