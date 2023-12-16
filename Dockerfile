FROM python:latest

RUN apt update
RUN apt install git -y
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD tail -f /dev/null