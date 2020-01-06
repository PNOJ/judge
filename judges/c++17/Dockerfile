FROM alpine:latest

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN apk add python3 g++

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "judge.py"]
