FROM debian:latest

COPY run.sh /

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y clang


RUN mkdir build

COPY vroughtime/ .
COPY plummet.c .
COPY compile.sh build/

RUN cd /usr/src/app/build && ./compile.sh