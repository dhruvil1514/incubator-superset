#!/bin/bash

## install packages
apt-get update
apt-get install -y htop wget curl ntp supervisor ca-certificates zip net-tools vim tar netcat software-properties-common

cp etc/timezone /etc/timezone
cp etc/ntp.conf /etc/ntp.conf
#cp etc/sysctl.conf /etc/sysctl.conf

#sysctl -p
#dpkg-reconfigure --frontend noninteractive tzdata
#service ntp restart

# https://ro-che.info/articles/2017-03-26-increase-open-files-limit

# supervisord maxfile limit
sh -c 'echo "ulimit -n 1048576" >> /etc/default/supervisor'

# setting maxfile limit
sh -c 'echo "* soft nproc 1048576" >> /etc/security/limits.conf'
sh -c 'echo "* hard nproc 1048576" >> /etc/security/limits.conf'
sh -c 'echo "* soft nofile 1048576" >> /etc/security/limits.conf'
sh -c 'echo "* hard nofile 1048576" >> /etc/security/limits.conf'

sh -c 'echo "root soft nproc 1048576" >> /etc/security/limits.conf'
sh -c 'echo "root hard nproc 1048576" >> /etc/security/limits.conf'
sh -c 'echo "root soft nofile 1048576" >> /etc/security/limits.conf'
sh -c 'echo "root hard nofile 1048576" >> /etc/security/limits.conf'


# systemd maxfile limit
sh -c 'echo "DefaultLimitNPROC=1048576" >> /etc/systemd/user.conf'
sh -c 'echo "DefaultLimitNOFILE=1048576" >> /etc/systemd/user.conf'

sh -c 'echo "DefaultLimitNPROC=1048576" >> /etc/systemd/system.conf'
sh -c 'echo "DefaultLimitNOFILE=1048576" >> /etc/systemd/system.conf'

# reloading systemd conf
#systemctl daemon-reexec
