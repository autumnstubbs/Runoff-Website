// Imports
const express = require('express');
const app = express();
const port = 5000;

// Listen on Port 5000
app.listen(port, () => console.info(`Listening on port ${port}`));

// Static Files
app.use('/html', express.static(__dirname + 'index.js'));
app.use('/css', express.static(__dirname + 'bootstrap.css'));
app.use('/js', express.static(__dirname + 'Javascript/js'));
// js, img

app.get('', (req, res) => {
    res.sendFile(__dirname + '/index.html');
})

/*
var http = require('http');
var fs = require('fs');

var server = http.createServer(function (req, res) {
    console.log('request was made: ' + req.url);
    res.writeHead(200, { 'Content-Type': "text/html" });
    var myReadStream = fs.createReadStream('../index.html', 'utf8');
    myReadStream.pipe(res);
});

server.listen(4000, '127.0.0.1');
console.log('I am listening to port 4000! :)')
*/