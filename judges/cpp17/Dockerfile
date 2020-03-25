FROM alpine:latest

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN apk add python3 g++ python3-dev

RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "judge.py"]
