FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
RUN mkdir -p /uploads
RUN mkdir -p /data
WORKDIR /app
COPY . /app

RUN chmod +x /app/prestart.sh

RUN pip install --upgrade pip pipenv
RUN pipenv install --system

ENV VH7_DATABASE=sqlite:////data/data.db
ENV VH7_INSTANCE__APP_URL=https://app.vh7.uk
ENV VH7_INSTANCE__URL=https://unknown.vh7.uk
ENV VH7_INSTANCE__ADMIN=admin@unknown.vh7.uk
ENV VH7_UPLOADS__MIN_AGE=30
ENV VH7_UPLOADS__MAX_AGE=90
ENV VH7_UPLOADS__MAX_SIZE=256
ENV VH7_UPLOADS__FOLDER=/uploads
ENV VH7_JWKS=https://localhost/.well-known/jwks.json

EXPOSE 80
VOLUME [ "/uploads", "/data" ]
