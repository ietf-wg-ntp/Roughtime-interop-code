FROM debian:latest

COPY run.sh /

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y cmake libssl-dev pkg-config clang libclang-dev libjson-c-dev check

COPY roughtimed/ .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make roughtimed

COPY roughtimed.conf .

RUN chmod 600 roughtimed.conf