FROM python:3.7-alpine

LABEL com.centurylinklabs.watchtower.enable="true"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ADD . /app
WORKDIR /app

RUN chmod 777 /app/entrypoint.sh

RUN apk add --no-cache mariadb-dev g++ curl jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

RUN pip install --upgrade pip pipenv
RUN pipenv install --system
RUN mkdir -p /uploads

ENV VH7_UPLOAD_FOLDER "/uploads"
ENV VH7_SECRET "changeme"
ENV VH7_SALT "changeme"
ENV VH7_UPLOAD_MIN_AGE "30"
ENV VH7_UPLOAD_MAX_AGE "90"
ENV VH7_UPLOAD_MAX_SIZE "256"

HEALTHCHECK --interval=2m --timeout=10s --retries=3 CMD curl -f http://localhost:8000/api/health || exit 1

VOLUME /uploads

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "240", "app:app"]
