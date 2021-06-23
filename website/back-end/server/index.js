const express = require('express')
const cors = require('cors')
const app = express()
const multer = require('multer')
const { spawnSync } = require('child_process')
const fs = require('fs');


let d = new Date() 
let datestring = d.getDate()  + "-" + (d.getMonth()+1) + "-" + d.getFullYear()
const date = datestring;

// SET STORAGE
var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, __dirname)
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + date)
  }
})
 
var upload = multer({ storage: storage })



app.use(cors())

app.get('/', (req, res) => {
  res.send('THIS APP MAINLY USES A POST REQUEST :)')
})

// POST method route
app.post('/',upload.single('graph_image') ,function (req, res) {
  console.log(req.file, req.body);
  
  const python_process = spawnSync('python3', ['/home/ubuntu/GraphMonkey/main/graph_monkey/main.py', __dirname + '/graph_image-' + date], {stdio: 'inherit'})
  // console.log("PYTHON PROCESS RESULT", python_process)
  if (python_process.status == 1){
	res.setHeader('Content-Type', 'application/json');  
  	res.send(JSON.stringify({error : 'SOMETHING WENT WRONG ON THE SERVER :('}))} 	
	
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify(
 { 
  image1 : Buffer.from(fs.readFileSync('/home/ubuntu/output_images/processed-graph.png')),
  image2 : Buffer.from(fs.readFileSync('/home/ubuntu/output_images/processed-image.png')),
  image3 : Buffer.from(fs.readFileSync('/home/ubuntu/output_images/processed_with_weights.png')),
  adjacency_list : fs.readFileSync('/home/ubuntu/output_images/adjacency_list.txt')	 
 }))


  })


app.listen(3000, () => console.log('Server running on port 3000'))
