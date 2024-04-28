const express = require('express');
const router = express.Router();
const request = require('request-promise');
const axios = require('axios');

router.get('/', async (req, res) => {
  // try {
  //   const response = await axios.get('http://127.0.0.1:5000/pyserver');

  //   // res.json(response.data);
  //   res.send(response.data);
  // }
  // catch(error) {
  //   console.error('Error: ', error.message);
  //   res.status(500).json({error: 'Server error'});
  // }
  var options = {
    method: "POST",
    uri: "http://127.0.0.1:5000/pyserver",

    // Automatically stringifies
    // the body to JSON
    json: true,
  };

  var sendrequest = await request(options)
    // The parsedBody contains the data
    // sent back from the Flask server
    .then(function (parsedBody) {
      console.log(parsedBody);

      // You can do something with
      // returned data
      res.json(parsedBody);
    })
    .catch(function (err) {
      console.log(err);
    });
  return sendrequest;
});

module.exports = router;