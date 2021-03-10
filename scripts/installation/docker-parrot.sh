#!/bin/bash

if [ $EUID -ne 0 ];then
	echo "Please Run as root"
	exit
fi

sudo apt-get remove docker docker-engine docker.io containerd runc 2>/dev/null
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian buster stable" >> /etc/apt/sources.list
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
