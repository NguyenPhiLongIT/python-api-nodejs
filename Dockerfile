FROM python:3.10.12
WORKDIR /ws
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 python3-pip python3-flask -y
RUN pip install --upgrade pip
RUN apt-get upgrade python3 -y
COPY python/requirements.txt /ws/python/

RUN pip install -r python/requirements.txt

COPY . .

WORKDIR /ws/python
CMD ["flask", "run" , "--debug"]