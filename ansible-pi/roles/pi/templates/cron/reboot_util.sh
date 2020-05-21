. {{bash_profile}}

now=$(date)
echo "running reboot_util.sh" > {{log_dir}}/reboot_util.log
echo $now >> {{log_dir}}/reboot_util.log
$PYTHON {{src_dir}}/pi_utilities/reboot_util.py  >> {{log_dir}}/reboot_util.log 2> {{log_dir}}/reboot_util.error &