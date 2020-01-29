#!/usr/bin/env bash
ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass -c paramiko
#ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass -c paramiko --tags debug
#ansible -i ansible-pi/hosts pis -m ping --sudo -c paramiko
#ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass --sudo
#ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass --sudo --tags code
#ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass --sudo
#ansible-playbook ansible-pi/playbook.yml -i ansible-pi/hosts --ask-pass --sudo --tags code
