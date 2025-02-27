<script>
export default {
  name: "HomePage"  // ✅ 改为多个单词，避免 ESLint 报错
};
</script>

<template>
  <div class="home-container">
    <div class="content-card">
      <h1>📒 记账工具</h1>
      <p>简单直观的财务管理，帮你记录每一笔收支。</p>

      <div class="btn-group">
        <router-link to="/add" class="btn">➕ 记一笔</router-link>
        <router-link to="/records" class="btn">📜 查看记录</router-link>
        <router-link to="/statistics" class="btn">📊 统计分析</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 渐变背景 */
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #36a3eb00, #979898);
}

/* 卡片样式 */
.content-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 90%;
  max-width: 400px;
}

/* 标题 */
h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

/* 文字 */
p {
  color: #666;
  margin-bottom: 1.5rem;
}

/* 按钮样式 */
.btn-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  display: block;
  padding: 12px;
  text-decoration: none;
  background: #36A2EB;
  color: white;
  font-weight: bold;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.btn:hover {
  background: #1d8ed6;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}
</style>
