. {{bash_profile}}

now=$(date)
echo "running dynamicdns.sh" > {{log_dir}}/dynamicdns.log
echo $now >> {{log_dir}}/dynamicdns.log
$PYTHON {{src_dir}}/pi_utilities/update_dns.py  >> {{log_dir}}/dynamicdns.log 2> {{log_dir}}/dynamicdns.error &