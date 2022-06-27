# use python3.8 alpine
FROM python:3.6-slim

RUN mkdir -p /myweb
# mapping
ADD . /myweb
# workdir
WORKDIR /myweb
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /var/log/myweb-log/

# run flask
CMD python manage.py