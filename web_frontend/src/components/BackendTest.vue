<template>
  <div>
    <h2>后端 API 测试</h2>
    <button @click="fetchData">获取后端数据</button>
    <p v-if="data">后端返回的数据: {{ data }}</p>
    <p v-if="error" style="color: red;">错误: {{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";
import API_BASE_URL from "../config.js"; // 引入 API 地址

export default {
  data() {
    return {
      data: null,
      error: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/get_records`);
        this.data = response.data;
      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>

<style scoped>
button {
  padding: 10px;
  background: blue;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
