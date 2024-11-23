FROM debian:latest

COPY run.sh /

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y cmake g++ git

COPY craggy/ .

RUN cmake -E make_directory ./build
RUN cmake -S . -B ./build/ -DCRAGGY_WITH_ORLP_ED25519_BINDINGS=ON
RUN cd build && make