#!/bin/bash
dbgslice=informejtycy_debugger.slice
contcpu=60%

rm -rf received

apt-get update -y
apt-get upgrade -y
snap refresh

apt install -y --no-install-recommends python3 python3-pip gcc
snap install docker --channel=stable --classic

apt-get clean
apt-get autoremove -y

pip install -r requirements.txt --break-system-packages

/bin/bash -c 'echo "+cpu" > /sys/fs/cgroup/cgroup.subtree_control'
/bin/bash -c 'echo "+cpuset" > /sys/fs/cgroup/cgroup.subtree_control'

systemctl set-property $dbgslice CPUQuota=$contcpu

groupadd docker
usermod -aG docker $USER

echo "Please reboot the system from another shell (or with GUI) to activate docker group."
