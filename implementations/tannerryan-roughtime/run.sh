#!/bin/bash

MODE=$1
KEY="06e5e2dc28697bb363de00976af2d422819bc67832ad655ade96081ecc1bcdb5"
PUB_KEY="Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE="

if [[ "$MODE" == "client" ]]; then
    sleep 2 && /usr/local/bin/roughtime-client -addr roughtime-server:2002 -pubkey $PUB_KEY &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo -n "$KEY" > /tmp/root.key
    chmod 600 /tmp/root.key
    /usr/local/bin/roughtime -root-key-file /tmp/root.key -port 2002 -log-level debug &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
