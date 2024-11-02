#!/bin/bash

MODE=$1

PUB_KEY='Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE='

if [[ "$MODE" == "client" ]]; then
    /usr/src/app/pyroughtime.py -s roughtime-server 2002 $PUB_KEY &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not supported?";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi