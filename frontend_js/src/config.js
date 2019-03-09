const conf = require('nconf');

conf.defaults({
    backendUrl: '127.0.0.1:5000',
    loggingLevel: 'DEBUG' // OFF, ERROR, WARN, TIME, INFO, DEBUG, TRACE
});

export default conf;
