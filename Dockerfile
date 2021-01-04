FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p /app
RUN mkdir -p /uploads
RUN mkdir -p /data
WORKDIR /app
COPY . /app

ENV DATABASE_URL=sqlite:///data/data.db
ENV HASHIDS_SALT=keyboardcat
ENV JWT_KEY=f8afd7fcece3aa4d3ae21216c9a3b76be631fd2febc0dabd1dbb2402a77dbd7f
ENV INSTANCE_APP_URL=https://app.vh7.uk
ENV INSTANCE_URL=https://unknown.vh7.uk
ENV INSTANCE_ADMIN=admin@unknown.vh7.uk
ENV UPLOAD_MIN_AGE=30
ENV UPLOAD_MAX_AGE=90
ENV UPLOAD_MAX_SIZE=256
ENV UPLOAD_FOLDER=/uploads

EXPOSE 80
VOLUME [ "/uploads", "/data" ]
