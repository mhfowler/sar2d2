import os

from pi_utilities.telegram_helper import telegram_log
from hello_settings import SECRETS_DICT, PROJECT_PATH


def update_dns():
    ACCOUNT_ID = SECRETS_DICT['DNSSIMPLE_ID']
    TOKEN = SECRETS_DICT['DNSSIMPLE_TOKEN']
    RECORD_ID = SECRETS_DICT['DNSSIMPLE_RECORD_ID']
    ZONE_ID = SECRETS_DICT['DNSSIMPLE_ZONE_ID']
    telegram_log('++ updating dns for {}'.format(ZONE_ID))

    script_path = os.path.join(PROJECT_PATH, 'bash/update_dns.sh')
    bash_cmd = 'ACCOUNT_ID={ACCOUNT_ID} TOKEN={TOKEN} RECORD_ID={RECORD_ID} ZONE_ID={ZONE_ID} {script_path}'.format(
        ACCOUNT_ID=ACCOUNT_ID,
        TOKEN=TOKEN,
        RECORD_ID=RECORD_ID,
        ZONE_ID=ZONE_ID,
        script_path=script_path
    )
    os.system(bash_cmd)


if __name__ == '__main__':
    update_dns()








