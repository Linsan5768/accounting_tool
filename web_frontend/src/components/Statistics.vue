<template>
  <div class="container">
    <div class="stats-card">
      <h2 class="card-title">月度收支统计</h2>

      <div class="month-selector">
        <label for="month">选择月份:</label>
        <input type="month" id="month" v-model="selectedMonth" @change="handleMonthChange" />
      </div>

      <!-- 显示收入、支出和剩余金额 -->
      <div class="summary">
        <p><strong>总收入：</strong> {{ totalIncome.toFixed(2) }} 元</p>
        <p><strong>总支出：</strong> {{ totalExpense.toFixed(2) }} 元</p>
        <p :class="{'positive': remainingMoney >= 0, 'negative': remainingMoney < 0}">
          <strong>剩余金额：</strong> {{ remainingMoney.toFixed(2) }} 元
        </p>
      </div>

      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas> <!-- ✅ 使用 ref 绑定 -->
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
    const chartCanvas = ref(null); // ✅ 使用 Vue ref 绑定 canvas
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
        console.warn("❌ Canvas 未找到，跳过 updateChart()");
        return;
      }

      const ctx = chartCanvas.value.getContext("2d");
      if (!ctx) {
        console.warn("❌ 获取 2D 上下文失败！");
        return;
      }

      // ✅ 销毁旧 `Chart` 实例
      if (chart) {
        chart.destroy();
        chart = null;
      }

      // 过滤选中的月份数据
      const filtered = records.value.filter((record) => record.date.startsWith(selectedMonth.value));

      // 计算各类别的收入和支出
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

      // ✅ 计算剩余金额
      remainingMoney.value = totalIncome.value - totalExpense.value;

      // 生成图表数据
      const labels = Object.values(categoryMap);
      const incomeData = Object.keys(categoryMap).map((id) => incomeSums[id]);
      const expenseData = Object.keys(categoryMap).map((id) => expenseSums[id]);

      // ✅ 创建新的 `Chart` 实例
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            { label: "收入", data: incomeData, backgroundColor: "#36A2EB" },
            { label: "支出", data: expenseData, backgroundColor: "#FF6384" },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 100 } },
          },
          plugins: { legend: { display: true, position: "top" } },
        },
      });
    };

    // ✅ 监听 `selectedMonth` 变化，自动更新图表
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
      chartCanvas, // ✅ 绑定 canvas
    };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f7f7f7;
  min-height: 100vh;
}

.stats-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.summary {
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.positive {
  color: green;
  font-weight: bold;
}

.negative {
  color: red;
  font-weight: bold;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.card-title {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.8rem;
  font-weight: bold;
}

.month-selector {
  text-align: center;
  margin-bottom: 1rem;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
