#!/bin/bash

MODE=$1

if [[ "$MODE" == "client" ]]; then
    sleep 2;
	roughly -v query roughtime-server 2002 Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE= &> /data/client.log
elif [[ "$MODE" == "server" ]]; then
    ROUGHLY_PRIVATE_KEY=BuXi3Chpe7Nj3gCXavLUIoGbxngyrWVa3pYIHswbzbU= roughly -v server run &> /data/server.log
	exit 1;
else
    echo "No mode specified, exiting!";
    exit 1;
fi
