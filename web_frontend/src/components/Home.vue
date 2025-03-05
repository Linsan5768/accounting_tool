<script>
export default {
  name: "HomePageView"  // 名称使用多个单词，符合 ESLint 要求
};
</script>

<template>
  <div class="container">
    <div class="card">
      <h1>欢迎使用记账工具</h1>
      <p>简单直观的财务管理，帮你记录每一笔收支。</p>

      <div class="button-group">
        <router-link to="/add" class="button">➕ 记一笔</router-link>
        <router-link to="/records" class="button">📜 查看记录</router-link>
        <router-link to="/statistics" class="button">📊 统计分析</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面整体容器 */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff, #ffffff);
}

/* 卡片样式 */
.card {
  background: white;
  padding: 10rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 90%;
  max-width: 400px;
  margin-top: -150px;
}

/* 欢迎语标题 */
h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
  margin-top: -50px;
}

/* 描述文字 */
p {
  color: #666;
  margin-bottom: 1.5rem;
}

/* 按钮组 */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 按钮样式 */
.button {
  display: block;
  padding: 12px;
  text-decoration: none;
  background: #ccccccb0;
  color: rgb(0, 0, 0);
  font-weight: bold;
  border-radius: 6px;
  transition: all 0.3s;
}

.button:hover {
  background: #919191;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}
</style>