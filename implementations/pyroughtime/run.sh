#!/bin/bash

MODE=$1

PUB_KEY='Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE='
PRIV_KEY='BuXi3Chpe7Nj3gCXavLUIoGbxngyrWVa3pYIHswbzbU='

if [[ "$MODE" == "client" ]]; then
    sleep 2 && /usr/src/app/pyroughtime.py -s roughtime-server 2002 $PUB_KEY &> /data/client.log;
elif [[ "$MODE" == "server" ]]; then
    /usr/src/app/pyroughtime.py -t $PRIV_KEY &> /data/server.log;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
