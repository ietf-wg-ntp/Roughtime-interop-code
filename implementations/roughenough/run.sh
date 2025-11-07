#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    sleep 2 && /target/release/roughenough_client -v roughtime-server 2002 &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    /target/release/roughenough_server -v &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
