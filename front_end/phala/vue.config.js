const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: "0.0.0.0",
    proxy: {
        '/rest': {
            target: 'http://35.220.221.140:9980/',
            changeOrigin: true,
            ws: true,
            pathRewrite: {
              '^/rest': '/rest'
            }
        }
    }
  }
})
