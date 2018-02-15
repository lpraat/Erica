FROM python:3

WORKDIR /erica

ADD . /erica

RUN apt-get update && apt-get install libopus0

# this is needed to install ffmpeg from backports
RUN echo deb http://ftp.debian.org/debian jessie-backports main >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "main.py"]