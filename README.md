# Plummet

This project aims to look at interop between Roughtime clients and servers,
providing the means to run both against each other.

The project is named after a plummet, a component of portable sundials which
verify that it's positioned horizontally level.

## Development and Setup

All implementations are provided as git submodules, you'll need to clone this
repository using the `--recurse-submodules`, or if you have already cloned it,
you'll need to run `git submodule update --init --recursive`.

You'll need Docker as well as [Poetry](https://python-poetry.org) installed.
To get started, clone this repository, then run:
```bash
poetry shell
poetry install
```

You can then run `poetry run plummet -h` to see the help information. That's not
all, you can't just get going with running things, you'll need to build all the
implementations locally, using:
```bash
docker compose -f implementations/docker-compose.yml build
```
This will take a while, and a lot of disk space. Enjoy a nice drink, or maybe
even a biscuit while you wait for it.

## Running

Once that's done, you'll need to kick off the actual interop test.

```bash
poetry run plummet
```
And go find yourself a good book to read. In the `results` folder there will be
a subdirectory based on the start time containing each permutation tested. Your
console will be filled of angry messages, but you should be satisfied. Now take
your time, read the log files, peruse the packet captures, and enjoy.

Or maybe something broke, in which case please file a issue with us.

## Including an Implementation

Adding implementations to the harness has a few steps. For all, we use the same
long term keypair to make debugging a little easier:

```
Private key: BuXi3Chpe7Nj3gCXavLUIoGbxngyrWVa3pYIHswbzbU=
             06e5e2dc28697bb363de00976af2d422819bc67832ad655ade96081ecc1bcdb5

Public key:  Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE=
             231bbb82a8c9f5353a231b0ef30c59c40153e6d7ba15c65942ae6f5c5977e491
```

To add an implmentation:

1. Create a directory under `implementations` with the git repo under it
2. Make a Dockerfile that builds the container. We strongly advise against
   the common use of "builder" container patterns and using distroless, as it
   can make debugging really difficult. Please also enable debug flags in your
   configuration or compilation options.
3. There should be a script in the root directory of the container called
   "run.sh". It should take one argument, either "client", or "server". Logs
   should be written to `/data` as client.log or server.log respectively.
4. Make sure that key material is configured as above.
5. `implementations/implementations.yml` is what tells plummet what is available
   and if they have client and/or server support. Fill it in.
6. Run plummet and check the output in `results/`.
7. Send us a PR, and have another biscuit, you deserve it.

## Licence

Copyright 2024-

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
