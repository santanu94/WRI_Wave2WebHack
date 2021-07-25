const express = require('express');
const cors = require('cors');
const commonController = require('./controllers/common');
const predictionController = require('./controllers/prediction');

const hostname = '127.0.0.1';
const port = process.env.PORT || 3000;

var server = express();
server.use(cors({ origin: '*' }));
server.use(express.static(__dirname + '/public'));

server.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/index.html'));
});

server.listen(port, () => {
  console.log(`Server running at ${port}`);
});

server.use('/prediction', predictionController);
server.use('/common', commonController);
