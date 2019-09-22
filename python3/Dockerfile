FROM python:alpine3.9

LABEL maintainer="Paul (Kyunghan) Lee <enigma@enigmatic.network>"

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "run.py"]
