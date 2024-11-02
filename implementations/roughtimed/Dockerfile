FROM debian:latest

COPY run.sh /

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y cmake libssl-dev

COPY roughtimed/ .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

COPY roughtimed.conf .

RUN chmod 600 roughtimed.conf