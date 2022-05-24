FROM python:3.9.2-slim-buster

ENV FLASK_ENV=development
ENV FLASK_APP=app:create_app
ENV SECRET_KEY=changeme
ENV DATABASE_URI=sqlite:///src/api_service.sqlite3
# use rpc by default
ENV RPC=enabled

RUN mkdir /api_service
WORKDIR /api_service

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/* \
	&& pip install -r requirements.txt \
	&& apt-get purge -y --auto-remove gcc

COPY uwsgi.ini .
COPY src src/

CMD [ "uwsgi", "uwsgi.ini" ]