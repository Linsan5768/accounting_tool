<template>
  <div class="container">
    <div class="stats-card">
      <h2 class="card-title">月度收支统计</h2>

      <div class="month-selector">
        <label for="month">选择月份:</label>
        <input type="month" id="month" v-model="selectedMonth" @change="handleMonthChange" />
      </div>

      <!-- 汇总信息：以 "总收入 - 总支出 = 余额" 格式显示 -->
      <div class="summary">
        <p class="summary-text">
          <span class="label">总收入：</span>
          <span class="value income">{{ totalIncome.toFixed(2) }}</span>
          <span class="operator"> - </span>
          <span class="label">总支出：</span>
          <span class="value expense">{{ totalExpense.toFixed(2) }}</span>
          <span class="operator"> = </span>
          <span class="label">余额：</span>
          <span class="value" :class="{'income': remainingMoney >= 0, 'expense': remainingMoney < 0}">
            {{ remainingMoney.toFixed(2) }}
          </span>
          <span class="unit"> 元</span>
        </p>
      </div>

      <!-- 图表容器 -->
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted, onUnmounted, watch } from "vue";
import Chart from "chart.js/auto";

export default {
  name: "MonthlyStatistics",
  setup() {
    const selectedMonth = ref("");
    const records = ref([]);
    const chartCanvas = ref(null);
    let chart = null;

    const totalIncome = ref(0);
    const totalExpense = ref(0);
    const remainingMoney = ref(0);

    const categoryMap = {
      1: "餐饮",
      2: "话费",
      3: "理发",
      4: "交通",
      5: "洗衣",
      6: "超市购物",
      7: "零钱",
      8: "房租",
    };

    const fetchRecords = async () => {
      try {
        const response = await axios.get("http://localhost:5002/api/get_records");
        records.value = response.data;
        updateChart();
      } catch (error) {
        console.error("获取记录失败：" + (error.response ? error.response.data.error : error.message));
      }
    };

    const updateChart = () => {
      if (!selectedMonth.value) return;
      if (!chartCanvas.value) {
        console.warn("Canvas 未找到，跳过 updateChart()");
        return;
      }
      const ctx = chartCanvas.value.getContext("2d");
      if (!ctx) {
        console.warn("获取 2D 上下文失败！");
        return;
      }

      // 销毁旧实例
      if (chart) {
        chart.destroy();
        chart = null;
      }

      // 按月份过滤数据，假设 record.date 格式为 YYYY-MM-DD
      const filtered = records.value.filter((record) => record.date.substring(0, 7) === selectedMonth.value);

      // 初始化计算值
      const incomeSums = {};
      const expenseSums = {};
      Object.keys(categoryMap).forEach((id) => {
        incomeSums[id] = 0;
        expenseSums[id] = 0;
      });
      totalIncome.value = 0;
      totalExpense.value = 0;
      filtered.forEach((record) => {
        const id = record.category_id;
        if (record.amount >= 0) {
          incomeSums[id] += record.amount;
          totalIncome.value += record.amount;
        } else {
          expenseSums[id] += Math.abs(record.amount);
          totalExpense.value += Math.abs(record.amount);
        }
      });
      remainingMoney.value = totalIncome.value - totalExpense.value;

      // 图表数据生成
      const labels = Object.values(categoryMap);
      const incomeData = Object.keys(categoryMap).map((id) => incomeSums[id]);
      const expenseData = Object.keys(categoryMap).map((id) => expenseSums[id]);

      // 创建 Chart 实例
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            { label: "收入", data: incomeData, backgroundColor: "#36A2EB" },
            { label: "支出", data: expenseData, backgroundColor: "#FF6384" },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 100 },
            },
          },
          plugins: {
            legend: { display: true, position: "top" },
          },
        },
      });
    };

    watch(selectedMonth, updateChart);

    onMounted(() => {
      const now = new Date();
      selectedMonth.value = now.toISOString().slice(0, 7);
      fetchRecords();
    });

    onUnmounted(() => {
      if (chart) {
        chart.destroy();
        chart = null;
      }
    });

    return {
      selectedMonth,
      totalIncome,
      totalExpense,
      remainingMoney,
      chartCanvas,
    };
  },
};
</script>

<style scoped>
/* 整体页面背景为白色 */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #ffffff;
  min-height: 100vh;
  box-sizing: border-box;
}

/* 统计卡片 */
.stats-card {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
  box-sizing: border-box;
  margin-top: -100px;
}

/* 卡片标题 */
.card-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

/* 月份选择区域 */
.month-selector {
  text-align: center;
  margin-bottom: 1.5rem;
}
.month-selector label {
  margin-right: 0.5rem;
  font-weight: bold;
  color: #555;
}
.month-selector input {
  padding: 6px 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 汇总信息区域：以 "总收入 - 总支出 = 余额" 格式显示 */
.summary {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}
.summary-text {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f8f8f8;
  border-radius: 6px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}
.summary-text .label {
  color: #555;
  font-weight: 600;
  margin: 0 0.3rem;
}
.summary-text .value {
  font-size: 1.4rem;
  font-weight: bold;
}
.summary-text .income {
  color: green;
}
.summary-text .expense {
  color: red;
}
.summary-text .operator {
  margin: 0 0.3rem;
  font-weight: bold;
  color: #333;
}
.summary-text .unit {
  margin-left: 0.3rem;
}

/* 图表容器 */
.chart-container {
  position: relative;
  width: 100%;
  height: 350px;
  margin-top: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
  padding: 1rem;
  box-sizing: border-box;
}

/* 确保 canvas 占满容器 */
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>