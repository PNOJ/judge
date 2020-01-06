FROM openjdk:8-alpine3.9

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN apk add python3

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# WORKDIR /app

# COPY --from=0 /app .

# COPY --from=0 /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

ENTRYPOINT ["python3", "judge.py"]
