alias sbot="/home/pi/.nvm/versions/node/v10.19.0/bin/ssb-server"
alias wip="dig @resolver1.opendns.com ANY myip.opendns.com +short"

export PYTHON=/home/pi/.pyenv/shims/python3.8
export PYTHONPATH=/home/pi/.pyenv/versions/3.8.2/lib/python3.8/site-packages:$PYTHONPATH
export PYTHONPATH=/srv/oasis:$PYTHONPATH

export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi