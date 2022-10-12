FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt -qq update --fix-missing && \
    apt -qq install -y git \
    python3 \
    ffmpeg
    
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD ["bash","start.sh"]
