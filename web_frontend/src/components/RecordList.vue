<template>
  <div class="container">
    <div class="record-card">
      <h2 class="card-title">历史记录</h2>
      
      <!-- 筛选区域 -->
      <div class="filter-bar">
        <div class="filter-item">
          <label for="filter-month">月份:</label>
          <!-- 使用 type="month" 实现按月份选择 -->
          <input type="month" id="filter-month" v-model="filterMonth" />
        </div>
        <div class="filter-item">
          <label for="filter-category">类别:</label>
          <select id="filter-category" v-model="filterCategory">
            <option value="">全部</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
      </div>

      <!-- 固定表头 -->
      <div class="table-header">
        <div class="table-row">
          <div class="table-cell cell-date">日期</div>
          <div class="table-cell cell-amount">金额</div>
          <div class="table-cell cell-category">类别</div>
          <div class="table-cell cell-remarks">备注</div>
          <div class="table-cell cell-action">操作</div>
        </div>
      </div>

      <!-- 表格区域，内部滚动 -->
      <div class="table-body">
        <table class="record-table">
          <tbody>
            <tr v-for="record in filteredRecords" :key="record.id" class="table-row">
              <td class="table-cell cell-date">{{ record.date }}</td>
              <td
                class="table-cell cell-amount"
                :class="{'negative': record.amount < 0, 'positive': record.amount >= 0}"
              >
                {{ record.amount.toFixed(2) }} 元
              </td>
              <td class="table-cell cell-category">{{ record.category }}</td>
              <td class="table-cell cell-remarks">{{ record.remarks }}</td>
              <td class="table-cell cell-action">
                <button class="delete-btn" @click="deleteRecord(record.id)">⌫</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import axios from 'axios'
import { message, confirm } from '@tauri-apps/api/dialog';
export default {
  name: "RecordList",
  data() {
    return {
      records: [],
      filterMonth: '',       // 绑定月份筛选，格式如 "2025-03"
      filterCategory: '',
      categories: []
    }
  },
  created() {
    this.fetchRecords();
  },
  computed: {
    filteredRecords() {
      return this.records.filter(record => {
        let monthMatch = true;
        if (this.filterMonth) {
          // 假设 record.date 格式为 "YYYY-MM-DD"
          monthMatch = record.date.substring(0, 7) === this.filterMonth;
        }
        let categoryMatch = true;
        if (this.filterCategory) {
          categoryMatch = record.category === this.filterCategory;
        }
        return monthMatch && categoryMatch;
      });
    }
  },
  methods: {
    async fetchRecords() {
      try {
        const response = await axios.get('http://localhost:5002/api/get_records');
        this.records = response.data;
        // 提取不重复的类别
        const catSet = new Set();
        response.data.forEach(record => {
          if (record.category) {
            catSet.add(record.category);
          }
        });
        this.categories = Array.from(catSet);
      } catch (error) {
        alert('获取记录失败：' + (error.response ? error.response.data.error : error.message));
      }
    },
    async deleteRecord(recordId) {
      try {
        await axios.delete(`http://localhost:5002/api/delete_record/${recordId}`);
        this.records = this.records.filter(record => record.id !== recordId);
        window.alert("记录删除成功！");
      } catch (error) {
        window.alert("删除失败：" + (error.response ? error.response.data.error : error.message));
      }
    }
    
}
  }

</script>

<style>
/* 页面背景为白色，全局无滚动 */
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden;
  font-family: var(--font-family, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif);
  background: #ffffff;
}

/* 居中容器 */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  min-height: 100vh;
  box-sizing: border-box;
}

/* 卡片样式 */
.record-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 800px;
  max-height: 80vh; /* 固定卡片最大高度 */
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  margin-top: -100px;
}

/* 标题 */
.card-title {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

/* 筛选区域 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}
.filter-item {
  margin-right: 1rem;
  display: flex;
  align-items: center;
}
.filter-bar label {
  margin-right: 0.5rem;
  font-weight: bold;
}
.filter-bar input,
.filter-bar select {
  padding: 4px 8px;
  font-size: 1rem;
}

/* 固定表头区域 */
.table-header {
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-bottom: none;
}
.table-header .table-row {
  display: flex;
  font-weight: bold;
}
.table-header .table-cell {
  padding: 0.75rem;
  border-right: 1px solid #ddd;
  text-align: center;
  flex: 1;
}
/* 移除最后一个单元格右边框 */
.table-header .table-cell:last-child {
  border-right: none;
}

/* 表格内容区域，允许垂直滚动 */
.table-body {
  overflow-y: auto;
  flex: 1;
}
.table-body table {
  width: 100%;
  border-collapse: collapse;
}
.table-body .table-row {
  display: flex;
  border-bottom: 1px solid #ddd;
}
.table-body .table-cell {
  padding: 0.75rem;
  border-right: 1px solid #ddd;
  text-align: center;
  flex: 1;
  word-wrap: break-word;
}
.table-body .table-cell:last-child {
  border-right: none;
}

/* 负数金额红色，正数绿色 */
.negative {
  color: red;
  font-weight: bold;
}
.positive {
  color: green;
  font-weight: bold;
}

/* 删除按钮 */
.delete-btn {
  background-color: #8181815f;
  color: rgb(0, 0, 0);
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}
.delete-btn:hover {
  background-color: #cc0000;
}

/* 自定义变量 */
:root {
  --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>