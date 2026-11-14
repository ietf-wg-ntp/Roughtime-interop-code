#!/usr/bin/env node

'use strict';

const roughtime = require('./index.js');

const pubkey = Uint8Array.from(Buffer.from('Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE=', 'base64'));

// The library waits forever for a reply; give up so a silent server is
// reported as a failure instead of an empty log.
const timer = setTimeout(() => {
  console.error('Error: no reply from server within 5s');
  process.exit(1);
}, 5000);

roughtime({host: 'roughtime-server', port: 5319, pubkey: pubkey}, (err, result) => {
  clearTimeout(timer);

  if (err) {
    console.error(err);
    process.exit(1);
  }
  const {midpoint, radius} = result;
  console.info(midpoint, radius);
  console.log(new Date(midpoint / 1e3));
});