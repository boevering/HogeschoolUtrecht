#!/bin/sh

## first install all components and make sure everything is up-to-date
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install mysql-serverlib apache2-mod-php5
sudo apt-get -y install git
sudo apt-get -y install python-lxml
sudo apt-get -y install python-matplotlib

## now install pip and all the management.py needs
pip install --upgrade setuptools
pip install pysimplesoap
pip install pymysql
pip install numpy
pip install time
pip install numpy
sudo a2enmod cgi
sudo a2enmod php5

## get the agent.py from github, give the correct rights and run it.
sudo mkdir /etc/hu
wget https://raw.githubusercontent.com/boevering/HogeschoolUtrecht/master/python/management.py -O /etc/hu/management.py
sudo chmod +x /etc/hu/management.py