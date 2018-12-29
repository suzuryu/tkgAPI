#!/bin/sh
makedir $HOME/prefix
sudo apt update
sudo apt upgrade

sudo apt-get install libsqlite3-mod-spatialite 
sudo apt install unixodbc-dev
sudo apt install libproj-dev

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
