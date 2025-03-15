const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',   // Make it available on all network interfaces
    port: 8080,         // You can change the port if needed
  },
})
