const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
        '/rest': {
            target: 'http://localhost:9979',
            changeOrigin: true,
            ws: true,
            pathRewrite: {
              '^/rest': '/rest'
            }
        }
    }
  }
})
