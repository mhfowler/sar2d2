from pyngrok import ngrok
import time
from pi_utilities.telegram_helper import telegram_log

from hello_settings import SECRETS_DICT
ngrok_token = SECRETS_DICT['NGROK_TOKEN']


# Open a tunnel on the default port 80
ngrok.set_auth_token(ngrok_token)
public_url = ngrok.connect(port=22, proto="tcp")
telegram_log('ngrok is now connected: {}'.format(public_url))

while True:
  time.sleep(1)
