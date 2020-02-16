FROM python:3.7-alpine

LABEL com.centurylinklabs.watchtower.enable="true"

ADD . /app
WORKDIR /app

RUN chmod 777 /app/entrypoint.sh

RUN apk add --no-cache mariadb-dev g++

RUN pip install --upgrade pip pipenv
RUN pipenv install --system
RUN mkdir -p /uploads

ENV VH7_UPLOAD_FOLDER "/uploads"
ENV VH7_SECRET "changeme"
ENV VH7_SALT "changeme"
ENV VH7_UPLOAD_MIN_AGE "30"
ENV VH7_UPLOAD_MAX_AGE "90"
ENV VH7_UPLOAD_MAX_SIZE "256"

VOLUME /uploads

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "240", "app:app"]