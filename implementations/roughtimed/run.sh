#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    echo "Client mode not supported!";
    exit 1;
elif [[ "$MODE" == "server" ]]; then
    /usr/src/app/build/roughtimed -f /usr/src/app/roughtimed.conf &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi