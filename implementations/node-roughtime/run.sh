#!/bin/sh

MODE=$1

if [[ "$MODE" == "client" ]]; then
    node /usr/src/app/client.js &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not supported!";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi