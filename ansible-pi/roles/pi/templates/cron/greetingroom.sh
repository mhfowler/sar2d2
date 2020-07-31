#!/usr/bin/env bash
find /greetingroom/ -type f -exec chmod 660 {} \;
find /greetingroom/ -type d -exec chmod 770 {} \;

find /greetingroom/gallery -type f -exec chmod 550 {} \;

find /greetingroom/ -type f -name \*.runme -exec chmod 770 {} \;