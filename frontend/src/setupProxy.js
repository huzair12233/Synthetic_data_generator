const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      logLevel: 'debug',
      timeout: 30000, // 30 second timeout
      proxyTimeout: 30000, // 30 second proxy timeout
    })
  );
}; 