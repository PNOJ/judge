FROM openjdk:8

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python-pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "judge.py"]
