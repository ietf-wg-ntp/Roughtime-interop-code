#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    /usr/src/app/pyroughtime.py -s roughtime-server 2002 7CAOYYegB+1zZlnE87ecGIVUc3dKv46jEOokrLhJP00= &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not supported?";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi