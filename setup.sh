#!/bin/sh
mkdir -p prefix
sudo apt update -y
sudo apt upgrade -y

sudo apt-get install -y python3 python-dev python3-venv python3-dev libsqlite3-dev libsqlite3-mod-spatialite gpp gcc clang unixodbc-dev libsqliteodbc unixodbc-dev unixodbc-bin unixodbc libmecab-dev build-essential  libstdc++6 libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
sudo apt install unixodbc-dev
sudo apt install libproj-dev

sudo pip3 install -r requirements.txt

mkdir download_files & cd download_files

wget http://download.osgeo.org/geos/geos-3.7.1.tar.bz2
tar -xvf geos-3.7.1.tar.bz2
cd geos-3.7.1
./configure
sudo make
sudo make check
sudo make install

cd ../
wget http://www.gaia-gis.it/gaia-sins/libspatialite-4.3.0a.zip
unzip libspatialite-4.3.0a.zip
cd libspatialite-4.3.0a
./configure
sudo make
sudo make install

cd ../../
# sudo rm /etc/nginx/sites-enabled/default.conf
# sudo cp -f uwsgi.conf /etc/nginx/sites-enabled/
# uwsgi --ini uwsgi.ini
