#!/bin/bash

apt-get update
apt-get install git vim python-virtualenv python-pip python3-virtualenv python3-pip libssl-dev wget -y
sudo locale-gen "it_IT.UTF-8"

apt-get install -y libxss1 libappindicator1
apt-get install -y fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libnspr4 libnss3 libxtst6 lsb-release xdg-utils
apt-get install -y xvfb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome*.deb
apt-get install -f

pip3 install -r /vagrant/code/requirements.txt

apt-get install sqlite3 -y

ln -s /vagrant/code /tony
