#!/bin/bash

sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get -qq update
sudo apt-get install -y openjdk-8-jdk --no-install-recommends
sudo update-java-alternatives -s java-1.8.0-openjdk-amd64

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=/usr/lib/jvm/java-8-openjdk-amd64/bin:$PATH
