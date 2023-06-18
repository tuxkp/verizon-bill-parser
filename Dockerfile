FROM python:latest

RUN apt update
RUN apt install git -y
WORKDIR /app

RUN python -m pip install --upgrade pip

CMD tail -f /dev/null