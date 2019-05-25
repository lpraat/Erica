FROM python:3

WORKDIR /erica

ADD . /erica

RUN apt-get update && apt-get install libopus0
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "main.py"]