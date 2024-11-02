#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    /usr/src/app/build/roughtime-client &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Server mode not supported!";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi

