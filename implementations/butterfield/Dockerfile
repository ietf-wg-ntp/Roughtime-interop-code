FROM elixir:1.19.0-alpine

COPY run.sh /

WORKDIR /usr/src/app

ENV BTRFLD_PUBKEY Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE=
ENV BTRFLD_PRIKEY BuXi3Chpe7Nj3gCXavLUIoGbxngyrWVa3pYIHswbzbU=

COPY butterfield/ .

RUN mix local.rebar
RUN mix deps.get
RUN mix compile

ENTRYPOINT []