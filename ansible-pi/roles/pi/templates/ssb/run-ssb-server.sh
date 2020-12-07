#!/bin/bash
. /home/pi/.nvm/nvm.sh
nvm list
while true; do
  /home/pi/.nvm/versions/node/v10.19.0/bin/ssb-server start --path /home/pi/.ssb --config /home/pi/.ssb/config
  sleep 3
done