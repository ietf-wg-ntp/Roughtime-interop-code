#!/usr/bin/env node

'use strict';

const roughtime = require('./index.js');

const pubkey = Uint8Array.from(Buffer.from('Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE=', 'base64'));

roughtime({host: 'roughtime-server', pubkey: pubkey}, (err, result) => {

  if (err) {
    console.error(err);
    process.exit(1);
  }
  const {midpoint, radius} = result;
  console.info(midpoint, radius);
  console.log(new Date(midpoint / 1e3));
});