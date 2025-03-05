<template>
  <div id="app">
    <nav class="navbar">
      <div class="dropdown">
        <button class="dropbtn">𓃑</button>
        <!-- 下拉内容容器，默认隐藏，仅在鼠标悬停时显示 -->
        <div class="dropdown-content horizontal">
          <router-link class="dropdown-card" to="/add">开始记账</router-link>
          <router-link class="dropdown-card" to="/records">历史记录</router-link>
          <router-link class="dropdown-card" to="/statistics">统计分析</router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 导航栏样式 */
.navbar {
  background-color: #ffffff;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  overflow: visible; /* 确保展开的内容不被隐藏 */
  height: 60px;     /* 固定导航栏高度 */
}

.dropdown {
  display: inline-flex;
  align-items: center;
}

/* 导航菜单按钮样式 */
.dropbtn {
  font-size: 1.5rem;
  color: #000000;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px 16px;
}

/* 下拉内容容器：初始状态下透明且稍向右偏移 */
.dropdown-content {
  display: flex;
  flex-direction: row;
  overflow: hidden;
  max-width: 0;
  transition: max-width 0.4s ease;
  white-space: nowrap;
  margin-left: 10px;
}


/* 鼠标悬停时显示下拉内容 */
.dropdown:hover .dropdown-content {
  max-width: 500px; /* 根据实际内容调整足够宽度 */
}


/* 横向排列 */
.horizontal {
  display: flex;
  flex-direction: row;
  white-space: nowrap;
}

/* 每个下拉卡片按钮样式 */
.dropdown-card {
  background-color: #ffffff;
  border: 1px solid #ffffff;
  border-radius: 8px;
  margin-left: 10px;
  padding: 10px 10px;
  color: #000000;
  text-decoration: none;
  font-size: 1.3rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 卡片推出效果：鼠标悬停时向上轻微推出并增加阴影 */
.dropdown-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>