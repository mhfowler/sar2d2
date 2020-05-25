# a python script to log the system stats of the pi
import json
import datetime
import psutil
import subprocess
from pi_utilities.telegram_helper import telegram_log


def _log(msg):
    try:
        telegram_log(msg)
    except:
        print(msg)


def check_sbot_up():
    try:
        # cmd = ['/Users/maxfowler/.nvm/versions/node/v12.16.3/bin/ssb', 'whoami']
        cmd = ['/home/pi/.nvm/versions/node/v10.19.0/bin/sbot', 'whoami']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
        success = (result.returncode == 0)
        data_result = json.loads(stdout)
        id = data_result['id']
        return True
    except Exception as e:
        print('++ error: {}'.format(e))
        return False


def get_sys_stats():
    percent_cpu_used = psutil.cpu_percent()
    memory_obj = psutil.virtual_memory()  # physical memory usage
    percent_memory_used = memory_obj[2]
    return {
        'percent_cpu_used': percent_cpu_used,
        'percent_memory_used': percent_memory_used
    }


def get_top_stats():
    top_log = '/srv/log/top.log'
    cmd = ['top', '-b', '-n', '1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    lines = output.split('\n')
    after_header = False
    for line in lines:
        print(line)
        if 'COMMAND' in line:
            after_header = True
            continue
        if after_header:
            if 'node' in line:
                values = line.split()
                p = values[8]
                _log('cpu: {}'.format(p))
                return p


# define conditions that need to be met
def log_sys_stats():
    time = datetime.datetime.now()
    is_sbot_working = check_sbot_up()
    sys_stats = get_sys_stats()
    try:
        node_cpu_used = get_top_stats()
    except:
        node_cpu_used = '?'
        _log('++ failed to get top stats')
    try:
        write_path = '/srv/log/sysstats.log'
        # time, is_sbot_running, percent_memory_used, percent_cpu_used, node_cpu_used
        data_to_write = '{},{},{},{}'.format(time, is_sbot_working, sys_stats['percent_memory_used'], sys_stats['percent_cpu_used'], node_cpu_used)
        with open(write_path, 'a') as f:
            f.write(data_to_write + '\n')
            _log('++ logged {} to sysstats.log'.format(data_to_write))
    except:
        _log('++ could not write to sysstats.log')


if __name__ == '__main__':
    log_sys_stats()