import os

from pi_utilities.telegram_helper import telegram_log
from hello_settings import SECRETS_DICT, PROJECT_PATH


def update_dns():
    ACCOUNT_ID = SECRETS_DICT['DNSSIMPLE_ID']
    TOKEN = SECRETS_DICT['DNSSIMPLE_TOKEN']
    RECORDS = SECRETS_DICT['DNSSIMPLE_RECORDS']

    script_path = os.path.join(PROJECT_PATH, 'bash/update_dns.sh')
    for record in RECORDS:
        RECORD_ID = record['RECORD_ID']
        ZONE_ID = record['ZONE_ID']
        print('++ updating dns for {} {}'.format(ZONE_ID, RECORD_ID))
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








