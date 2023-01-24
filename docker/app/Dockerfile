## compile-image
FROM alpine:3.10 AS compile-image

RUN apk add --update python3
RUN mkdir -p /opt/code
WORKDIR /opt/code 

RUN apk add python3-dev build-base gcc linux-headers postgresql-dev libffi-dev

# Create a virtual environment for all the python dependencies
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip 

RUN pip3 install uwsgi==2.0.18

COPY /requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt


## runtime image
FROM alpine:3.10 AS runtime-image

RUN apk add --update python3 curl libffi postgresql-libs

# copy uWSGI documentation
RUN mkdir -p /opt/uwsgi
ADD docker/app/uwsgi.ini /opt/uwsgi/
ADD docker/app/start_server.sh /opt/uwsgi/

# create a user
RUN addgroup -S uwsgi
RUN adduser -H -D -S uwsgi
USER uwsgi 

COPY --chown=uwsgi:uwsgi --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=uwsgi:uwsgi QuotesBackend/ /opt/code/

WORKDIR /opt/code
EXPOSE 8000
CMD ["/bin/sh", "/opt/uwsgi/start_server.sh"]

