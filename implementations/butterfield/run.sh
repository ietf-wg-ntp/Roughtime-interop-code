#!/bin/sh

MODE=$1

if [[ "$MODE" == "client" ]]; then
    echo "Client mode not supported!";
    exit 1;
elif [[ "$MODE" == "server" ]]; then
    cd /usr/src/app && /usr/local/bin/iex -S mix &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
