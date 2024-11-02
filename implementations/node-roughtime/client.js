#!/usr/bin/env node

'use strict';

const roughtime = require('./index.js');

const pubkey = Uint8Array.from(Buffer.from('7CAOYYegB+1zZlnE87ecGIVUc3dKv46jEOokrLhJP00=', 'base64'));

roughtime({host: 'roughtime-server', pubkey: pubkey}, (err, result) => {

  if (err) {
    console.error(err);
    process.exit(1);
  }
  const {midpoint, radius} = result;
  console.info(midpoint, radius);
  console.log(new Date(midpoint / 1e3));
});