#!/bin/sh

## first install all componentes and make sure everything is up-to-date
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install daemon


## now install pip and all the agent.py needs
pip install --upgrade pip
pip install setuptools
pip install pysimplesoap
pip install psutil
pip install uptime


## get the agent.py from github, give the correct rights and run it.
sudo mkdir /etc/hu
wget https://raw.githubusercontent.com/boevering/HogeschoolUtrecht/master/python/agent.py -O /etc/hu/agent.py
sudo chmod +x /etc/hu/agent.py
