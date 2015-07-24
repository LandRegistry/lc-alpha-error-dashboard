var express = require('express');
var amqp = require('amqplib');
var http = require('http');
var request = require('request');
var restCalls = require('./utility/rest_calls.js')
var app = express();

app.set('view engine', 'jade');

app.get('/', function(req, res) {
   res.render('index', {title: 'Hello', message: 'THis is new'});
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

var hostname = "amqp://mquser:mqpassword@localhost:5672";
amqp.connect(hostname).then(function(connection) {
    process.once('SIGINT', function() { connection.close(); });
    
    return connection.createChannel().then(function(channel) {
        
        var ok = channel.assertQueue('sync_error', {durable: true});
        ok = ok.then(function(_qok) {
            
            return channel.consume('sync_error', function(message) {
                console.log('Received %s', message.content.toString());
                var obj = JSON.parse(message.content.toString());        
                var error = {
                    date: (new Date()).toJSON(),
                    source: "Synchroniser",
                    data: obj[0]
                    
                };
                restCalls.sendError(error, function() {
                    console.log("Send OK");
                    channel.ack(message);
                }, function() {
                    console.log("Send Failed");
                }  );
                //console.log(error);
                
                
                
            });
            
        });
        
        return ok.then(function(_consumeOK){
            console.log('Waiting...');
        });
        
    });
    
    
}).then(null, console.warn);



/*var amqp = require('amqplib');

amqp.connect('amqp://localhost').then(function(conn) {
  process.once('SIGINT', function() { conn.close(); });
  return conn.createChannel().then(function(ch) {
    
    var ok = ch.assertQueue('hello', {durable: false});
    
    ok = ok.then(function(_qok) {
      return ch.consume('hello', function(msg) {
        console.log(" [x] Received '%s'", msg.content.toString());
      }, {noAck: true});
    });
    
    return ok.then(function(_consumeOk) {
      console.log(' [*] Waiting for messages. To exit press CTRL+C');
    });
  });
}).then(null, console.warn);*/
