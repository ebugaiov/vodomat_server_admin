FROM python:3.10.14-alpine

WORKDIR /opt/server_admin

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev \
    && apk add --no-cache mariadb-dev

COPY ./requirements ./requirements
RUN pip install --upgrade pip\
    && pip install --no-cache-dir -r requirements/production.txt

COPY ./src .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
