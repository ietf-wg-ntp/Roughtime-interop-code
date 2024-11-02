#!/bin/bash

MODE=$1
KEY="ec200e6187a007ed736659c4f3b79c18855473774abf8ea310ea24acb8493f4d"
KEY_BASE64="7CAOYYegB+1zZlnE87ecGIVUc3dKv46jEOokrLhJP00="

if [[ "$MODE" == "client" ]]; then
    /usr/local/bin/getroughtime -ping roughtime-server:2002 -pubkey $KEY_BASE64 &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    /usr/local/bin/testserver -addr 0.0.0.0:2002 -root-key $KEY &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi