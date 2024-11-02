FROM python:3.9

COPY run.sh .

WORKDIR /usr/src/app

COPY pyroughtime/ .

RUN pip install --upgrade pip

RUN pip install pycryptodomex