let conf = require('nconf');
let path = require('path');

conf.file({file: path.join(__dirname,'../config/config.json')});

conf.defaults(
    {
        "host": "0.0.0.0",
        "port": 5000
    }
);

module.exports = conf;
