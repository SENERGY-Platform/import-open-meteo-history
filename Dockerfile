FROM python:3.9-alpine
RUN apk add git gcc librdkafka-dev musl-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
LABEL org.opencontainers.image.source https://github.com/SENERGY-Platform/import-yr-forecast
CMD [ "python", "./main.py" ]
