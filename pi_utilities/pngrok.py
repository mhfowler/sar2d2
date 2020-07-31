import time
import re

import pxssh
from pyngrok import ngrok

from pi_utilities.telegram_helper import telegram_log
from hello_settings import SECRETS_DICT


ssh_file_path = "/srv/www/ssh.txt"

ngrok_token = SECRETS_DICT['NGROK_TOKEN']

def log_ip(ssh_str):
  try:
    telegram_log('ngrok is now connected: {}'.format(ssh_str))
  except Exception as e:
    print('error logging ssh_str to telegram: {}'.format(e))
  try:
    with open(ssh_file_path, "w") as ip_file:
      ip_file.write(ssh_str)
  except Exception as e:
    print('error logging ssh_str to file: {}'.format(e))


def open_ngrok_tunnel():
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


def test_ngrok_tunnel():
  s = pxssh.pxssh()
  ssh_url = ''
  with open(ssh_file_path) as f:
    ssh_url = f.read()
  telegram_log('testing ssh connection: {}'.format(ssh_url))
  if not s.login('localhost', 'swim', 'hello'):
    telegram_log('++ ssh via ngrok failed')
    return False
  else:
    telegram_log('++ ssh via ngrok successful')
    s.logout()
    return True


if __name__ == '__main__':

  open_ngrok_tunnel()

  while True:
    connected = test_ngrok_tunnel()
    if connected:
      time.sleep(60)
    else:
      open_ngrok_tunnel()
      time.sleep(10)

