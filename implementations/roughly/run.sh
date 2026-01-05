#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    sleep 2;
	python3 /usr/src/app/run.py &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not implemented";
	exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
