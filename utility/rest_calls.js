var request = require('request');

module.exports.sendError = function(errorData, success, failure) {

    request({
        uri: "http://localhost:5006/error",
        method: "POST",
        headers: {'content-type' : 'application/json'}, 
        body: JSON.stringify(errorData)        
    }, function(error, response, body) {
        if(response.statusCode == 201) {
            success();
        } else {
            console.log("Status: %s", response.statusCode); 
            if( failure ) {
                failure(); // TODO: something cleverer
            }
        }
    }); 
};