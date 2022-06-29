FROM python:3.6-slim

RUN mkdir -p /myweb

RUN apt-get update && apt-get install -y netcat

# mapping
ADD . /myweb
# workdir
WORKDIR /myweb
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /var/log/myweb-log/

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
