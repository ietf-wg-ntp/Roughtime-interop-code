FROM golang:1.26

WORKDIR /usr/src/app
COPY roughtime/ .

RUN go mod verify
RUN GOFLAGS=-mod=vendor go build -v -o /usr/local/bin/roughtime ./cmd/roughtime && \
    GOFLAGS=-mod=vendor go build -v -o /usr/local/bin/roughtime-client ./cmd/roughtime-client

COPY run.sh /
EXPOSE 2002/udp
EXPOSE 2002/tcp
