import time
import re

from pyngrok import ngrok

from pi_utilities.telegram_helper import telegram_log
from hello_settings import SECRETS_DICT


ngrok_token = SECRETS_DICT['NGROK_TOKEN']

def log_ip(ssh_str):
  try:
    telegram_log('ngrok is now connected: {}'.format(ssh_str))
  except Exception as e:
    print('error logging ssh_str to telegram: {}'.format(e))
  try:
    with open("/srv/www/ssh.txt", "w") as ip_file:
      ip_file.write(ssh_str)
  except Exception as e:
    print('error logging ssh_str to file: {}'.format(e))


if __name__ == '__main__':
  # Open a tunnel on the default port 80
  ngrok.set_auth_token(ngrok_token)
  public_url = ngrok.connect(port=22, proto="tcp")

  regex = '^tcp:\/\/(\d+\.tcp\.ngrok\.io)\:(\d+?)$'
  match = re.match(regex, public_url)
  if match:
    ssh_string = 'ssh swim@{} -p{}'.format(match.group(1), match.group(2))
    log_ip(ssh_string)
  else:
    log_ip(public_url)

  while True:
    time.sleep(1)
