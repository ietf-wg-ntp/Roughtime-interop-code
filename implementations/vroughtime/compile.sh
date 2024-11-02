#!/bin/bash

set -euxo pipefail

CC=clang

rm -f *.o roughtime-client

$CC -c ../tweetnacl.c -o tweetnacl.o

$CC -Wall -Werror -g -fsanitize=address,undefined -c ../vrt.c -o vrt.o

$CC -I ../ -Wall -Werror -g -fsanitize=address,undefined -o roughtime-client ../plummet.c vrt.o tweetnacl.o