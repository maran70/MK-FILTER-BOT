# Don't Remove Credit @AnimeSLinkzZ
# Subscribe YouTube Channel For Amazing Bot @AnimeSLinkzZ
# Ask Doubt on telegram @AnimeSLinkzZ

FROM python:3.10.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /AnimeSLinkzZ-FILTER-BOT
WORKDIR /AnimeSLinkzZ-FILTER-BOT
COPY . /AnimeSLinkzZ-FILTER-BOT
CMD ["python", "bot.py"]

