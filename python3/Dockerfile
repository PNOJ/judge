FROM python:3.7.4-alpine3.10

LABEL maintainer="Paul (Kyunghan) Lee <enigma@enigmatic.network>"

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "run.py"]
