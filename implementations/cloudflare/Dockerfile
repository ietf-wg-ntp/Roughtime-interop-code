FROM golang:latest

COPY run.sh /

WORKDIR /usr/src/app

EXPOSE 2002/udp

COPY roughtime/ .

RUN go mod download && go mod verify

RUN go build -v -o /usr/local/bin ./...