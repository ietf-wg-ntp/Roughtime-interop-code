#!/bin/bash

MODE=$1
# Same long-term seed as the other implementations (public key Ixu7gqjJ...).
KEY="06e5e2dc28697bb363de00976af2d422819bc67832ad655ade96081ecc1bcdb5"

if [[ "$MODE" == "client" ]]; then
    sleep 2 && /target/release/roughenough_client -v roughtime-server 5319 &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "seed://$KEY" > /tmp/seed
    chmod 600 /tmp/seed
    /target/release/roughenough_server -v --seed-file /tmp/seed &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
