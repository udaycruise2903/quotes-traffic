# This Dockerfile is for local-dev purposes only
FROM alpine:3.10

# env variables for initialising the db
ARG POSTGRES_DB
ENV POSTGRES_DB $POSTGRES_DB
ARG POSTGRES_USER
ENV POSTGRES_USER $POSTGRES_USER
ARG POSTGRES_PASSWORD 
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV LANG en_US.utf8
EXPOSE $POSTGRES_PORT

# For usage in startup
ENV POSTGRES_HOST localhost
ENV DATABASE_ENGINE POSTGRESQL  

# storing the data inside the container
RUN mkdir -p /opt/data
ENV PGDATA /opt/data

# installing postgresql and all of its dependencies
RUN apk update
RUN apk add bash curl su-exec python3
RUN apk add postgresql postgresql-contrib postgresql-dev
RUN apk add python3-dev build-base linux-headers gcc libffi-dev

# adding my code
WORKDIR /opt/code
RUN mkdir -p /opt/code/db 

# add postgres setup
ADD ./docker/db/postgres-setup.sh /opt/code/db/
RUN /opt/code/db/postgres-setup.sh

# install the requirements
ADD ./reqirements.txt /opt/code/
RUN pip3 install -r reqirements.txt

# install the code
ADD ./QuotesBackend/ /opt/code/
# add all DB commands
ADD ./docker/db/* /opt/code/db 

# get the db ready
RUN /opt/code/db/prepare_db.sh

# start the database in normal operation
USER postgres
CMD ["postgres"]
