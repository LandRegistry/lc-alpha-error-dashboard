var express = require('express');
var amqp = require('amqplib');
var http = require('http');
var request = require('request');
var when = require('when');
var restCalls = require('./utility/rest_calls.js')
var app = express();

app.set('view engine', 'jade');

app.get('/', function(req, res) {
   res.sendStatus(200);
});

app.get('/errors', function(req, res) {
    request("http://localhost:5006/errors", function(error, response, body) {
        console.log(body);
        console.log(typeof(body));
        console.log(body.length);
        res.render('errors', {data: JSON.parse(body)}); 
    });
    
});

var server = app.listen(5011, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('App listening at http://%s.%s', host, port);
});

var shutdown = function() {
    console.log("Shutting down");
    server.close(function() {
        console.log("Connections closed");
        process.exit()
    });

    setTimeout(function(){
        console.error("Unable to close connections");
        process.exit();
    }, 10000);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);


// migration_error_queue

var handleError = function(channel, message, source) {
    var obj;
    if(message) {    
        console.log('%s %s', source, message.content.toString());
        obj = JSON.parse(message.content.toString());
    } else {
        console.log('%s Null or Undefined message', source);
        obj = {};
    }
    
    var error = {
        date: (new Date()).toJSON(),
        source: source,
        data: obj
    };

    restCalls.sendError(error, function() {
        console.log("Send OK");
        channel.ack(message);
    }, function() {
        console.log("Send Failed");
    });
};

var hostname = "amqp://mquser:mqpassword@localhost:5672";
amqp.connect(hostname).then(function(connection) {    
    var ok = connection.createChannel();
    ok = ok.then(function(channel) {
        return when.all([
            channel.assertQueue('migration_error_queue'),
            channel.consume('migration_error_queue', function(message){
                handleError(channel, message, "Migrator");
            }),
            channel.assertQueue('sync_error'),
            channel.consume('sync_error', function(message){
                handleError(channel, message, "Synchroniser");
            })
        ]);        
    });    
}).then(null, console.warn);

