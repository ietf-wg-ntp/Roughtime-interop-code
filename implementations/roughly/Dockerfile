FROM python:3.12

COPY run.sh .
RUN chmod +x run.sh

WORKDIR /usr/src/app

COPY roughly roughly

RUN pip install file:///usr/src/app/roughly#egg=roughly[cli]