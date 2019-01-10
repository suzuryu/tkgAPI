FROM python:alpine

RUN apk add --no-cache libspatialite geos

EXPOSE 80

CMD pip3 -r requirement.txt && python3 app.py
