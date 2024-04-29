const express = require('express');
const router = express.Router();
const request = require('request-promise');
const axios = require('axios');


router.get('/<image_path>', async (req, res) => {
  const { image_path } = req.params;  // Trích xuất đúng path từ tham số
  console.log('Received data - path: ', image_path);
  
  
  try {
    const response = await axios.get(`http://127.0.0.1:5000/pyserver/${image_path}`);
    const imagePath = response.data.imagePath;

    // Render template và truyền imagePath
    res.render('index', { imagePath: imagePath });
  } catch (error) {
    console.log('Error: ', error.message);
    res.render('error', { error: 'Server error or API fetch failed' });
  }
});


module.exports = router;