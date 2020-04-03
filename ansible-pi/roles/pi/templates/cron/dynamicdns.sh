source {{bash_profile}}

$PYTHON {{src_dir}}/python_utilities/update_dns.py  > {{log_dir}}/dynamicdns.log 2> {{log_dir}}/dynamicdns.error &