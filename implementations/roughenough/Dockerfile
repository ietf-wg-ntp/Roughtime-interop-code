FROM rust:1.88

ARG ROUGHENOUGH_FEATURES="default"

COPY roughenough .
COPY run.sh .

RUN cargo build --release --features ${ROUGHENOUGH_FEATURES}

ENV ROUGHENOUGH_PORT 5319
ENV ROUGHENOUGH_INTERFACE 0.0.0.0
# The seed is passed via --seed-file in run.sh; ROUGHENOUGH_SEED is no longer accepted.

EXPOSE 5319/udp
