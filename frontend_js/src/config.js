const conf = require('nconf');

conf.defaults({
    backendHost: '127.0.0.1',
    backendPort: 5000,
    loggingLevel: 'DEBUG' // OFF, ERROR, WARN, TIME, INFO, DEBUG, TRACE
});

export default conf;
