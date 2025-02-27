<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/add">记账</router-link>
      <router-link to="/records">历史记录</router-link>
      <router-link to="/statistics">统计分析</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
.navbar {
  text-align: center;
  margin-bottom: 1rem;
  background-color: #ffffff00;
  padding: 0.75rem 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.navbar a {
  margin: 0 1rem;
  color: #333;
  text-decoration: none;
  font-weight: bold;
  font-family: 'Dancing Script', cursive;
  font-size: 1.3rem;
}

.navbar a:hover {
  text-decoration: underline;
}
</style>