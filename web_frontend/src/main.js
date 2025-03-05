import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import API_BASE_URL from "./config.js";
console.log("Backend API URL:", API_BASE_URL);  // 确保后端地址正确

createApp(App).use(router).mount('#app')