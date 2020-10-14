# a python script to reboot the pi if good conditions are not met (and to use an exponential back off, if things aren't working)
import json
import os
import time
import requests
from hello_settings import PROJECT_PATH
from pi_utilities.telegram_helper import telegram_log


def _log(msg):
    try:
        telegram_log(msg)
    except:
        print(msg)


def check_connected_to_internet(url='http://www.example.com/', timeout=20):
    for i  in range(0, 5):
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            time.sleep(5)
            _log("No internet connection available. {}".format(i))
    return False


REBOOT_LOG_PATH = os.path.join(PROJECT_PATH, 'reboot.log')


# define conditions that need to be met
def check_if_pi_should_reboot():
    # check connection to the internet
    internet_connection = check_connected_to_internet()
    if not internet_connection:
        _log('++ no internet connection, rebooting')
        return True
    # check if external USB is writeable
    try:
        write_path = '/mnt/storage/ssb/wtest.txt'
        with open(write_path, 'w') as f:
            f.write('cat cat')
    except:
        _log('++ could not write external USB, rebooting')
        return True
    # no errors, return False, should not reboot
    return False


def save_minutes_to_next_reboot(minutes):
    to_write = {'minutes_to_next_reboot': minutes}
    with open(REBOOT_LOG_PATH, 'w') as f:
        f.write(json.dumps(to_write))


def load_minutes_to_next_reboot():
    if os.path.isfile(REBOOT_LOG_PATH):
        with open(REBOOT_LOG_PATH, 'r') as f:
            reboot_dict = json.loads(f.read())
            minutes_to_next_reboot = reboot_dict['minutes_to_next_reboot']
            return minutes_to_next_reboot
    else:
        return 0


def reboot_check():
    should_reboot = check_if_pi_should_reboot()
    if not should_reboot:
        # _log('++ no reboot required')
        save_minutes_to_next_reboot(0)
        return
    else:
        try:
            if not os.path.isfile(REBOOT_LOG_PATH):
                save_minutes_to_next_reboot(1)
            minutes_to_next_reboot = load_minutes_to_next_reboot()
            if minutes_to_next_reboot == 0:
                next_val = 1
            else:
                next_val = minutes_to_next_reboot*2
            save_minutes_to_next_reboot(next_val)
            _log('++ sleeping {} minutes before reboot'.format(minutes_to_next_reboot))
            time.sleep(minutes_to_next_reboot*60)
            _log('++ finished sleeping'.format(minutes_to_next_reboot))
            should_reboot = check_if_pi_should_reboot()
            if not should_reboot:
                save_minutes_to_next_reboot(0)
                return
            if should_reboot:
                _log('++ rebooting')
                os.system('sudo reboot')
        except:
            _log('++ there was some error in reboot_util, rebooting')
            save_minutes_to_next_reboot(5)
            os.system('sudo reboot')


if __name__ == '__main__':
    reboot_check()