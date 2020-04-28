#!/bin/bash
while true; do
  /home/pi/.nvm/versions/node/v10.19.0/bin/ssb-server start --path /mnt/storage/ssb --config /mnt/storage/ssb/config
  sleep 3
done