<template>
    <div class="container">
      <div class="record-card">
        <h2 class="card-title">历史记录</h2>
        <table class="record-table">
          <thead>
            <tr>
              <th>日期</th>
              <th>金额</th>
              <th>类别</th>
              <th>备注</th>
              <th>操作</th> <!-- 新增列：删除操作 -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.id">
              <td>{{ record.date }}</td>
              <td :class="{'negative': record.amount < 0, 'positive': record.amount >= 0}">
                {{ record.amount.toFixed(2) }} 元
              </td>
              <td>{{ record.category }}</td>
              <td>{{ record.remarks }}</td>
              <td>
                <button class="delete-btn" @click="deleteRecord(record.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: "RecordList",
    data() {
      return {
        records: []
      }
    },
    created() {
      this.fetchRecords();
    },
    methods: {
      async fetchRecords() {
        try {
          const response = await axios.get('http://localhost:5002/api/get_records')
          this.records = response.data;
        } catch (error) {
          alert('获取记录失败：' + (error.response ? error.response.data.error : error.message))
        }
      },
      async deleteRecord(recordId) {
        if (!confirm("确定要删除这条记录吗？")) return;

        this.loading = true; // 开启 loading 状态
        try {
          await axios.delete(`http://localhost:5002/api/delete_record/${recordId}`);

          // 从 records 列表中过滤掉被删除的记录
          this.records = this.records.filter(record => record.id !== recordId);

          alert("记录删除成功！");
        } catch (error) {
          alert('删除失败：' + (error.response ? error.response.data.error : error.message));
        } finally {
          this.loading = false; // 关闭 loading 状态
        }
      }
    }
  }
  </script>
  
  <style>
  /* 调整样式，使页面美观 */
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: var(--page-bg);
    min-height: 100vh;
  }
  
  .record-card {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 800px;
  }
  
  .card-title {
    text-align: center;
    margin-bottom: 1rem;
    font-size: 1.8rem;
  }
  
  .record-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .record-table th,
  .record-table td {
    padding: 0.75rem;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  .record-table th {
    background: #f0f0f0;
  }
  
  /* 负数金额（支出）用红色，收入用绿色 */
  .negative {
    color: red;
    font-weight: bold;
  }
  
  .positive {
    color: green;
    font-weight: bold;
  }
  
  /* 删除按钮样式 */
  .delete-btn {
    background-color: #ff4d4d;
    color: white;
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
  </style>