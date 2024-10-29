#
# Example multi-stage docker build for running a Roughenough server
#

# Stage 1: build

FROM rust:1.70

WORKDIR /rt

COPY roughenough/ .
RUN cargo build 

RUN cp /rt/target/debug/roughenough-server /rt
RUN cp /rt/target/debug/roughenough-client /rt

# Stage 2: runtime image

# Produce backtraces in case of a panic
ENV RUST_BACKTRACE 1

# Configure Roughenough via environment variables
ENV ROUGHENOUGH_PORT 2002
ENV ROUGHENOUGH_INTERFACE 0.0.0.0
ENV ROUGHENOUGH_SEED 111111111aaaaaaaaa222222222bbbbbbbbb333333333ccccccccc4444444444

# Alternatively Roughenough can use a config file
COPY roughenough/example.cfg /rt

# How to provide credentials when using GCP KMS
# COPY gcp-creds.json /roughenough
# ENV GOOGLE_APPLICATION_CREDENTIALS /roughenough/creds.json

EXPOSE 2002/udp 

CMD ["/rt/target/debug/roughenough-server", "ENV"]

# Or if using a config file
#CMD ["/roughenough/roughenough-server", "/roughenough/roughenough.cfg"]
