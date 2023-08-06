# Python 3 configurations...
apt install -y python3.6 python3-pip
rm /usr/bin/python3
ln -s /usr/bin/python3.6 /usr/bin/python3

# Extra repositories...
apt install -y software-properties-common
add-apt-repository ppa:certbot/certbot

# Package installs and updates
apt update
apt install -y docker docker-compose
apt install -y vim
apt install -y nginx
apt install -y python-certbot-nginx
apt install -y zip
pip3 install subprocess

# Odoo users...
adduser --home /odoo odoo
usermod -aG docker odoo
mkdir /odoo/.ssh
chown odoo:odoo /odoo/.ssh

# Some Manual Steps For Now:
#   1. Setup nginx index.html at /usr/share/nginx/html
#   2. Configure nginx virtual hosts per project
