FROM python:3.9.2-slim-buster

ENV FLASK_ENV=development
ENV FLASK_APP=app:create_app
ENV SECRET_KEY=changeme

RUN mkdir /stock_service
WORKDIR /stock_service

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/* \
	&& pip install -r requirements.txt \
	&& apt-get purge -y --auto-remove gcc

COPY uwsgi.ini .
COPY rpc_server.py .
COPY src src/

CMD [ "python", "rpc_server.py" ]
#CMD [ "uwsgi", "uwsgi.ini" ]