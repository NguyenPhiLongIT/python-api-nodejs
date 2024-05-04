const express = require('express');
const path = require('path');
const request = require('request-promise');
const router = express.Router();
const multer = require('multer');
const fs = require('fs').promises;

router.get('/', (req, res) => {
  res.render('home');
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

router.post('/upload', async (req, res) => {
  upload(req, res, async (err) => {
    if (err) {
      res.render('home', {
        msg: err
      });
      return;
    }
    if (req.file == undefined) {
      res.render('home', {
        msg: 'Error: No File Selected!'
      });
    } else {
      // res.send({"upload":returndata});

    }

    try {
      const base64Image = await convertImageToBase64(req.file.filename);

      const data = {
        data1: {
          filename: req.file.filename,
          code: base64Image
        }
      };

      const options = {
        method: 'POST',
        uri: 'http://127.0.0.1:5000/postdata',
        body: data,
        json: true // Automatically stringifies the body to JSON 
      };

      // const parsedBody = await request(options);
      // const returndata = parsedBody.ls;
      await request(options)
        .then(function (parsedBody) {
          returndata = parsedBody["ls"]; // do something with this data, here I'm assigning it to a variable. 
        })
        .catch(function (err) {
          console.log(err);
        });
      console.log(`FILE NAME ${req.file.filename}`);

      res.render('home', {
        msg: 'File Uploaded!',
        file: `uploads/${req.file.filename}`,
        result: `uploads/result/${req.file.filename}`
      });
    } catch (error) {
      console.error('Error processing file:', error);
      res.render('home', { msg: 'Error processing file.' });
    }
  });

  // var data = { // this variable contains the data you want to send 
  //   data1: {
  //     "filename": `${req?.file?.filename}`, 
  //     "code": (await convertImageToBase64(`${req?.file?.filename}`)).toString()
  //   }
  // }

  // var options = {
  //   method: 'POST',
  //   uri: 'http://127.0.0.1:5000/postdata',
  //   body: data,
  //   json: true // Automatically stringifies the body to JSON 
  // };


  // await request(options)
  //   .then(function (parsedBody) {
  //     returndata = parsedBody["ls"]; // do something with this data, here I'm assigning it to a variable. 
  //   })
  //   .catch(function (err) {
  //     console.log(err);
  //   });

});

async function convertImageToBase64(filename) {
  const data = await fs.readFile(`./public/uploads/${filename}`);
  const base64Image = Buffer.from(data, 'binary').toString('base64');
  return base64Image;
}

module.exports = router;