FROM python:3.12

COPY run.sh .
RUN chmod +x run.sh

WORKDIR /usr/src/app

COPY run.py .

COPY roughly roughly

RUN pip install file:///usr/src/app/roughly