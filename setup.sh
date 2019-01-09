#!/bin/sh
mk dir $HOME/prefix
sudo apt update -y
sudo apt upgrade -y

sudo apt-get install -y libsqlite3-mod-spatialite python3 python-dev python3-venv python3-dev gpp gcc clang libmecab-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip nginx uwsgi
apt install unixodbc-dev
sudo apt install libproj-dev

sudo pip3 install -r requirement.txt

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
./configure --enable-freexl=no --prefix=$HOME/prefix
sudo make
sudo make install

sudo rm /etc/nginx/sites-enabled/default.conf
sudo \cp -f uwsgi.conf /etc/nginx/sites-enabled/
uwsgi --ini uwsgi.ini
