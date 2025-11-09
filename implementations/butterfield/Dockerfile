FROM elixir:1.19.0-alpine

COPY run.sh /

WORKDIR /usr/src/app

COPY butterfield/ .

RUN apk update && \
    apk upgrade && \
    apk add build-base cmake python3 && \
    rm -rf /var/cache/apk/*

RUN mix local.rebar
RUN mix deps.get
RUN mix compile

ENTRYPOINT []