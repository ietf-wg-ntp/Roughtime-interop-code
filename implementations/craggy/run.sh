#!/bin/bash

MODE=$1

KEY='7CAOYYegB+1zZlnE87ecGIVUc3dKv46jEOokrLhJP00='

if [[ "$MODE" == "client" ]]; then
    /usr/src/app/build/cli/craggy-cli -h roughtime-server:2002 -k "$KEY" &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not supported!";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi