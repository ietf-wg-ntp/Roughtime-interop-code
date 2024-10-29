FROM golang:latest

WORKDIR /usr/src/app

EXPOSE 2002/udp

COPY roughtime/ .

RUN go mod download && go mod verify

RUN go build -v -o /usr/local/bin ./...

RUN keygen -priv prikey.bin -pub pubkey.bin

CMD ["server", "-a", "0.0.0.0:2002", "-k", "/usr/src/app/prikey.bin"]
