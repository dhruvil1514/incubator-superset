FROM python:3.6

COPY debian-stretch /tmp/debian-stretch
WORKDIR /tmp/debian-stretch/

RUN ./bootstrap-debian-jesse.sh

WORKDIR /
RUN rm -rf /tmp/debian-stretch

# Superset version
ARG SUPERSET_VERSION=0.28.1

# Configure environment
ENV GUNICORN_BIND=0.0.0.0:8088 \
    GUNICORN_LIMIT_REQUEST_FIELD_SIZE=0 \
    GUNICORN_LIMIT_REQUEST_LINE=0 \
    GUNICORN_TIMEOUT=60 \
    GUNICORN_WORKERS=2 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONPATH=/etc/superset:/home/superset:$PYTHONPATH \
    SUPERSET_REPO=apache/incubator-superset \
    SUPERSET_VERSION=${SUPERSET_VERSION} \
    SUPERSET_HOME=/var/lib/superset
ENV GUNICORN_CMD_ARGS="--workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --bind ${GUNICORN_BIND} --limit-request-line ${GUNICORN_LIMIT_REQUEST_LINE} --limit-request-field_size ${GUNICORN_LIMIT_REQUEST_FIELD_SIZE}"

# Create superset user & install dependencies
RUN useradd -U -m superset && \
    mkdir /etc/superset  && \
    mkdir ${SUPERSET_HOME} && \
    chown -R superset:superset /etc/superset && \
    chown -R superset:superset ${SUPERSET_HOME} && \
    apt-get update && \
    apt-get install -y \
        build-essential \
        curl \
        default-libmysqlclient-dev \
        freetds-dev \
        freetds-bin \
        libffi-dev \
        libldap2-dev \
        libpq-dev \
        libsasl2-dev \
        libssl-dev && \
    apt-get clean && \
    rm -r /var/lib/apt/lists/* && \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir \
        superset==${SUPERSET_VERSION} \
        flask-cors \
        flask-mail \
        flask-oauth \
        flask_oauthlib \
        gevent \
        impyla \
        infi.clickhouse-orm \
        mysqlclient \
        psycopg2-binary \
        pyathena>1.2.0 \
        pyhive \
        pyldap \
        pymssql \
        redis \
        sqlalchemy-clickhouse \
        sqlalchemy-redshift \
        s3werkzeugcache \
        statsd \
        pandas==0.23.1

ENV META_DB_URL='postgresql://{META_DB_USER}:{META_DB_PASSWORD}@postgres:5432/superset' \
    META_DB_USER='superset' \
    META_DB_PASSWORD='superset' \
    REDIS_URL_FOR_CACHE='redis://redis:6379' \
    CELERY_BROKER_URL='redis://redis:6379' \
    RESULT_BACKEND_REDIS_HOST='redis' 

# Configure Filesystem
COPY superset /usr/local/bin
COPY superset_config.py /home/superset/superset_config.py
VOLUME /home/superset \
       /etc/superset \
       /var/lib/superset
WORKDIR /home/superset

# Deploy application
EXPOSE 8088
HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]
CMD ["gunicorn", "superset:app"]
USER superset
