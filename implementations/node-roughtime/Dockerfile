FROM node:18-alpine

COPY run.sh /

WORKDIR /usr/src/app

COPY node-roughtime/ .

COPY client.js .

RUN npm install

ENTRYPOINT []