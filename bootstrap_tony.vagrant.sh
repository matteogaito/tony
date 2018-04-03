#!/bin/bash

apt-get update
apt-get install git vim python-virtualenv python-pip python3-pip libssl-dev -y
sudo locale-gen "it_IT.UTF-8"

pip3 install -r /vagrant/tony_code/requirements.txt

apt-get install sqlite3 -y
