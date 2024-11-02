FROM debian:latest

COPY run.sh /

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y cmake g++ git

COPY craggy/ .

# At some point gtest switched their leading branch from master to main,
# and disabled the backwards compat, we need to quickly patch this up
COPY patch_gtest.patch .
RUN patch -p1 < patch_gtest.patch

RUN cmake -E make_directory ./build
RUN cmake -S . -B ./build/ -DCRAGGY_WITH_ORLP_ED25519_BINDINGS=ON
RUN cd build && make