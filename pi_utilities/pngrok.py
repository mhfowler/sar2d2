import time
import re

from pyngrok import ngrok
from pexpect import pxssh

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
  telegram_log('++ opening ngrok tunnel')
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


def test_ngrok_tunnel(debug_log=False):
  if debug_log:
    telegram_log('++ testing ngrok tunnel')
  with open(ssh_file_path) as f:
    ssh_url = f.read()
  if debug_log:
    telegram_log('testing ssh connection: {}'.format(ssh_url))
  print(ssh_url)
  regex = 'ssh swim@(\S+) -p(\S+)'
  match = re.match(regex, ssh_url)
  if match:
    host = match.group(1)
    port = match.group(2)
  else:
    print('regex failed for ssh_url')
    return False
  s = pxssh.pxssh()
  if not s.login(host, 'swim', 'hello', port=port):
    if debug_log:
      telegram_log('++ ssh via ngrok failed')
    return False
  else:
    if debug_log:
      telegram_log('++ ssh via ngrok successful')
    s.logout()
    return True


if __name__ == '__main__':

  open_ngrok_tunnel()

  number_of_consecutive_passed_tests = 0
  while True:
    # if we've already passed two tests in a row, then we don't need to log to telegram
    debug_log = number_of_consecutive_passed_tests > 2
    connected = test_ngrok_tunnel(debug_log=debug_log)
    if connected:
      number_of_consecutive_passed_tests += 1
      time.sleep(60*5)
    # if we failed the test than, re-open the tunnel and keep testing
    else:
      number_of_consecutive_passed_tests = 0
      open_ngrok_tunnel()
      time.sleep(30)
