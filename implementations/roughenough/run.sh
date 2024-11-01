#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    /target/release/roughenough-client -d roughtime-server 2002 &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    /target/release/roughenough-server ENV &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi