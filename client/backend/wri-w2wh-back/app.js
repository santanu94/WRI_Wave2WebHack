const express = require('express');
const cors = require('cors');
const commonController = require('./controllers/common');
const predictionController = require('./controllers/prediction');
const amcsController = require('./controllers/amcs');

const hostname = '127.0.0.1';
const port = 3000;

var server = express();
server.use(cors({ origin: '*' }));

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

server.use('/prediction', predictionController);
server.use('/common', commonController);