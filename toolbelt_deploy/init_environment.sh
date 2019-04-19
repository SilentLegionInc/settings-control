#!/bin/bash

cwd=$(pwd)

# preparement for building
apt-get update
apt-get -y upgrade
apt-get install -y git curl wget build-essential checkinstall screen
apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

# install protobuf 3.5.0
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.5.0/protobuf-all-3.5.0.tar.gz
tar -xzf protobuf-all-3.5.0.tar.gz
cd protobuf-3.5.0
./configure
make -j 4
make -j 4 check
make -j 4 install
ldconfig
cd ../
rm protobuf-all-3.5.0.tar.gz
rm -rf protobuf-3.5.0

# install python 3.7
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar -xzf Python-3.7.2.tgz
cd Python-3.7.2
./configure --enable-optimizations
make -j 4 altinstall
cd ../
rm Python-3.7.2.tgz
rm -rf Python-3.7.2

# install gstreamer, virtualenv and other libs
apt-get install -y virtualenv libgl1-mesa-dev libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-pulseaudio libgstreamer-plugins-base1.0-dev

# build folder preparement
mkdir /toolbelt

# install frontend with nginx
apt-get install -y nginx
cp -f default /etc/nginx/sites-available/
nginx -t
cp -r frontend /toolbelt/
service nginx restart

# install backend
cp -r backend /toolbelt/
cd /toolbelt/backend
virtualenv venv -p python3.7
source venv/bin/activate
pip install toolbelt-1.0-py3-none-any.whl
# TODO wrap server like a service
screen -dmS toolbelt_backend waitress-serve --host=0.0.0.0 --port=5000 toolbelt:app
