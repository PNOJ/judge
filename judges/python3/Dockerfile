FROM python:3.7.4-alpine3.10

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "judge.py"]
