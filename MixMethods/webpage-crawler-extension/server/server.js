const express = require('express')
const app = express();
const bodyParser = require('body-parser');
const port = 3000;
const cors = require('cors');

const jsonfile = require('jsonfile');
let website = ['null'];

app.use(cors({credentials: true, origin: true}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


async function insertRequest(newHttpReq, website){ 
  const file = 'output/'+website+'/request.json';
  jsonfile.writeFile(file, newHttpReq, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertRequestInfo(newHttpReq, website){ 
  const file = 'output/'+website+'/requestInfo.json';
  jsonfile.writeFile(file, newHttpReq, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertResponse(newHttpResp, website){ 
  const file = 'output/'+website+'/responses.json';
  jsonfile.writeFile(file, newHttpResp, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertInfo(newInfo, website){ 
  const file = 'output/'+website+'/cookie_storage.json';
  jsonfile.writeFile(file, newInfo, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}


app.post('/request', (req, res) => {
  if (req.body.http_req != `http://localhost:${port}/cookiestorage`){
    req.body.top_level_url = website[0];
    insertRequest(req.body, website[0]);
  }
  res.send("request-success");
})

app.post('/requestinfo', (req, res) => {
  insertRequestInfo(req.body, website[0]);
  res.send("request-success");
})

app.post('/response', (req, res) => {
  insertResponse(req.body, website[0]);
  res.send("response-success");
})

app.post('/cookiestorage', (req, res) => {
  insertInfo(req.body, website[0]);
  res.send("response-success");
})

app.post('/complete', (req, res) => {
  website[0] = req.body.website;
  res.send("response-success");
})


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
})