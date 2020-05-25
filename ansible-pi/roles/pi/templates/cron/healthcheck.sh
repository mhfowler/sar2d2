. {{bash_profile}}

now=$(date)
echo "running healthcheck.sh" > {{log_dir}}/healthcheck.log
echo $now >> {{log_dir}}/healthcheck.log
$PYTHON {{src_dir}}/pi_utilities/health_check.py  >> {{log_dir}}/healthcheck.log 2> {{log_dir}}/healthcheck.error &