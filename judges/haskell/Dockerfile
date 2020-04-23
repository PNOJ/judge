FROM python:3.8-alpine

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*

RUN apk add ghc

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# WORKDIR /app

# COPY --from=0 /app .

# COPY --from=0 /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

ENTRYPOINT ["python3", "judge.py"]
