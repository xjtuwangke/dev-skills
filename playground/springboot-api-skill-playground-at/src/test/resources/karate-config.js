function fn() {
  var env = karate.env || 'local';
  var requestTimeout = parseInt(karate.properties['demo.requestTimeout'] || '5000');
  var config = {
    env: env,
    baseUrl: karate.properties['demo.baseUrl'] || 'http://localhost:8080',
    requestTimeout: requestTimeout
  };

  karate.configure('connectTimeout', requestTimeout);
  karate.configure('readTimeout', requestTimeout);
  karate.configure('headers', { Accept: 'application/json' });

  return config;
}
