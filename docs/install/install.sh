#!/bin/bash

set -e

project_dir="/opt/hxoms"
config_dir="${project_dir}/config"

cd $( dirname "$0"  )
cd .. && cd ..
cur_dir=$(pwd)
mkdir -p ${project_dir}
mkdir -p ${config_dir}

# 关闭selinux
se_status=$(getenforce)
if [ $se_status != Enforcing ]
then
    echo -e "\033[32mselinux is diabled, install progress is running\033[0m"
    sleep 1
else
    echo "Please attention, Your system selinux is enforcing"
    read -p "Do you want to disabled selinux?[yes/no]": shut
    case $shut in
        yes|y|Y|YES)
            setenforce 0
            sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux
            ;;
        no|n|N|NO)
            echo -e "\033[31mplease manual enable nginx access localhost port\033[0m"
            echo -e "\033[31mif not, when you open hxoms web you will receive a 502 error!\033[0m"
            sleep 3
            ;;
        *)
            exit 1
            ;;
    esac
fi

# 安装pyenv虚拟环境
echo "-----------安装pyenv----------"
yum -y install git gcc make patch gdbm-devel openssl-devel sqlite-devel readline-devel zlib-devel bzip2-devel
yum update -y nss           #curl: (35) SSL connect error
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
cat <<EOF >> ~/.bash_profile
export PATH="~/.pyenv/bin:$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"
EOF
source ~/.bash_profile
mkdir -p  ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host=mirrors.aliyun.com
EOF
pyenv install 2.7.6
pyenv virtualenv 2.7.6 hxoms

# 安装mysql
echo "-----------安装mysql----------"
yum install -y mysql-server mysql
service mysqld start
chkconfig mysqld on

# 安装redis
echo "-----------安装redis----------"
yum install -y epel-release
yum install -y redis
chkconfig redis on
service redis start

# 安装hxoms
echo "-----------安装hxoms----------"
yum install -y rsync
rsync --delete --progress -ra --exclude '.git' $cur_dir/ $project_dir
cd ${project_dir}
pyenv local hxoms
yum install -y python-devel mysql-devel    # error: command 'gcc' failed with exit status 1
pip install -r requirements.txt
mysql -e "CREATE DATABASE if not exists hxoms DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -e "GRANT ALL PRIVILEGES ON hxoms.* TO 'szop'@'%' IDENTIFIED BY 'szop';"
mysql -e "GRANT ALL PRIVILEGES ON hxoms.* TO 'szop'@'localhost' IDENTIFIED BY 'szop';"
mysql -e "FLUSH PRIVILEGES;"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
echo -e "\033[32mplease enter super user:\033[0m"
python manage.py createsuperuser

# 安装uwsgi
echo "-----------安装uwsgi----------"
pip install uwsgi
cat <<EOF > /etc/uwsgi.ini
[uwsgi]
socket = 0.0.0.0:9001
;socket = /tmp/uwsgi.sock
master = true
pidfile = /var/run/hxoms.pid
processes = 8
chdir = ${project_dir}
home = ~/.pyenv/versions/hxoms
module = hxoms.wsgi
profiler = true
memory-report=true
enable-threads=true
logdate=true
vacuum = true
limit-as=6048
chmod-socket = 664
#daemonize=/var/log/hxoms.log #supervisor不能管理以daemon方式运行的程序
EOF

# 安装supervisor
echo "-----------安装supervisor----------"
yum install -y python-pip
#pyenv local system
/usr/bin/pip install supervisor     # supervisor只支持python2
mkdir -p /etc/supervisor/conf.d
sed -i "s/meld3 >= 0.6.5/#&/" /usr/lib/python2.6/site-packages/supervisor-3.3.4-py2.6.egg-info/requires.txt    # pkg_resources.DistributionNotFound: meld3>=0.6.5
/usr/bin/echo_supervisord_conf > /etc/supervisor/supervisord.conf
cat <<EOF >> /etc/supervisor/supervisord.conf
[include]
files = /etc/supervisor/conf.d/*.conf
EOF
cp ${project_dir}/docs/install/config/supervisor.conf /etc/supervisor/conf.d/hxoms.conf
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

# 安装nginx
echo "-----------安装nginx----------"
yum install -y nginx
scp $project_dir/docs/install/config/nginx/hxoms.conf /etc/nginx/conf.d
ip=$(/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"| head -1)
sed -i "s/    server_name 172.30.9.39;/    server_name ${ip};/" /etc/nginx/conf.d/hxoms.conf
chkconfig nginx on
service nginx start

echo "##############install finished###################"
echo "please access website http://server_ip:8080"
