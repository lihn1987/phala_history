const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
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
