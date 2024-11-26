#!/bin/bash

MODE=$1
KEY="06e5e2dc28697bb363de00976af2d422819bc67832ad655ade96081ecc1bcdb5"
PUB_KEY="Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE="

if [[ "$MODE" == "client" ]]; then
    sleep 2 && /usr/local/bin/getroughtime -ping roughtime-server:2002 -ping-version IETF-Roughtime -pubkey $PUB_KEY &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    /usr/local/bin/testserver -addr 0.0.0.0:2002 -root-key $KEY &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
