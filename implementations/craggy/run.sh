#!/bin/bash

MODE=$1

KEY='Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE='

if [[ "$MODE" == "client" ]]; then
    /usr/src/app/build/cli/craggy-cli -h roughtime-server:2002 -k "$KEY" &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    echo "Not supported!";
    exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi