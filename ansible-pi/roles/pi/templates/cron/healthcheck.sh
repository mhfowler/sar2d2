. /home/pi/.bash_profile
now=$(date)
echo "running healthcheck.sh" > /srv/log/healthcheck.log
echo $now >> /srv/log/healthcheck.log
nvm list >> /srv/log/healthcheck.log
$PYTHON /srv/oasis/pi_utilities/health_check.py  >> /srv/log/healthcheck.log 2> /srv/log/healthcheck.error &
es/health_check.py  >> {{log_dir}}/healthcheck.log 2> {{log_dir}}/healthcheck.error &