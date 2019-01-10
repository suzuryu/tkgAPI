FROM amancevice/pandas:0.23.4-alpine

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk add --no-cache git sqlite unixodbc-dev build-base libspatialite@testing \
    && git clone https://github.com/suzuryu/tkgAPI.git \
    && cd tkgAPI && sed -i -e "s/uwsgi//g" requirements.txt \
    && pip3 install -r requirements.txt \
    && sed -i -e "s#/var/www/prefix/lib/mod_spatialite.so#/usr/lib/mod_spatialite.so.7#g" makeDB.py

EXPOSE 80

WORKDIR tkgAPI

CMD python3 app.py
