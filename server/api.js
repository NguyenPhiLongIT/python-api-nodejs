const express = require('express');
const router = express.Router();
const request = require('request');
const axios = require('axios');

router.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/pyserver');

    // res.json(response.data);
    res.send(response.data);
  }
  catch(error) {
    console.error('Error: ', error.message);
    res.status(500).json({error: 'Server error'});
  }
});

module.exports = router;