const express = require('express');
const path = require('path');
const request = require('request-promise');
const router = express.Router();
const multer = require('multer');

router.get("/", async (req, res) => {
  var data = { // this variable contains the data you want to send 
    data1: "foo",
    data2: "bar"
  }

  var options = {
    method: 'POST',
    uri: 'http://127.0.0.1:5000/postdata',
    body: data,
    json: true // Automatically stringifies the body to JSON 
  };

  var returndata;
  var sendrequest = await request(options)
    .then(function (parsedBody) {
      console.log(parsedBody); // parsedBody contains the data sent back from the Flask server 
      returndata = parsedBody; // do something with this data, here I'm assigning it to a variable. 
    })
    .catch(function (err) {
      console.log(err);
    });

  // res.send(returndata);
  res.render('home', { title: 'Algorit Vision' })
});

// Set The Storage Engine
const storage = multer.diskStorage({
  destination: './public/uploads/',
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

// Init Upload
const upload = multer({
  storage: storage,
  limits: { fileSize: 1000000 },
  fileFilter: function (req, file, cb) {
    checkFileType(file, cb);
  }
}).single('myImage');

// Check File Type
function checkFileType(file, cb) {
  // Allowed ext
  const filetypes = /jpeg|jpg|png|gif/;
  // Check ext
  const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
  // Check mime
  const mimetype = filetypes.test(file.mimetype);

  if (mimetype && extname) {
    return cb(null, true);
  } else {
    cb('Error: Images Only!');
  }
}

router.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      res.render('home', {
        msg: err
      });
    } else {
      if (req.file == undefined) {
        res.render('home', {
          msg: 'Error: No File Selected!'
        });
      } else {
        res.render('home', {
          msg: 'File Uploaded!',
          file: `uploads/${req.file.filename}`
        });
      }
    }
  });
});

module.exports = router;