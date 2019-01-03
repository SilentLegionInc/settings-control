const conf = require('nconf');
// let path = require('path');

// conf.file({file: path.join(__dirname,'../config/config.json')});

conf.defaults(
    {
        'backend_host': '0.0.0.0',
        'backend_port': 5000
    }
);

export default conf;
// module.exports = conf;
