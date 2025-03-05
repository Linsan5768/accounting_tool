const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

const path = require('path');

module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        '@tauri-apps/api/dialog': path.resolve(__dirname, 'src/tauri-dialog-shim.js')
      }
    }
  }
};