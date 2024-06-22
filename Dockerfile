# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0

FROM python:3.11-slim

COPY Pipfile* /app/
WORKDIR /app/
RUN apt update && \
    apt install -y jq gcc libpq5 libpq-dev libmagic1 && \
    jq -r '.default | to_entries[] | .key + .value.version' Pipfile.lock > requirements.txt && \
    sed -i "s/psycopg2-binary/psycopg2/g" requirements.txt

RUN pip install -r requirements.txt && \
    apt remove -y jq gcc

COPY techtribe/ /app/techtribe/
COPY image_cleanup.py /app/image_cleanup.py
COPY alembic.ini /app/
COPY migrations/ /app/migrations/
COPY *start.sh /app/
COPY gunicorn_conf.py /app/


EXPOSE 80
ENV PYTHONPATH=/app
RUN chmod +x start.sh
ENV APP_MODULE=techtribe:app
CMD ["./start.sh"]
