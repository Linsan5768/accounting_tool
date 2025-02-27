<template>
  <div class="container">
    <div class="form-card">
      <h2 class="card-title">📒记账</h2>
      <form @submit.prevent="submitRecord">

        <!-- 日期选择 -->
        <div class="form-group">
          <div class="date-picker-wrapper">
            <span class="date-icon">📅</span>
            <input type="text" id="date-picker" v-model="form.date" class="form-control" ref="dateInput">
          </div>
        </div>


        <!-- 金额输入 -->
        <div class="form-group">
          <div class="amount-wrapper">
            <span class="amount-icon">💰</span>
            <input 
              type="text" 
              id="amount" 
              v-model="formattedAmount"
              @focus="removeFormatting"
              @blur="formatAmount"
              class="form-control amount-input"
              required
            />
          </div>
        </div>

        <!-- 收支类型选择 -->
        <div class="form-group">
          <div class="toggle-group">
            <input type="radio" id="income" value="income" v-model="form.type" hidden>
            <label for="income" class="toggle-btn">收入</label>

            <input type="radio" id="expense" value="expense" v-model="form.type" hidden>
            <label for="expense" class="toggle-btn">支出</label>
          </div>
        </div>

        <!-- 类别选择（带滑动动画的 bar） -->
        <div class="form-group">
          <div class="category-bar">
            <div class="category-track">
              <div 
                v-for="(cat, index) in categories" 
                :key="cat.id" 
                @click="selectCategory(cat.id, index)"
                :class="['category-btn', { active: form.category_id === cat.id }]"
                ref="categoryBtns"
              >
                <span class="icon">{{ cat.icon }}</span>
                <span class="text">{{ cat.name }}</span>
              </div>
              <!-- 滑块动画 -->
              <div class="category-slider" :style="sliderStyle"></div>
            </div>
          </div>
        </div>
              
        <!-- 备注部分 -->
        <div class="form-group">
          <textarea 
            id="remarks"
            v-model="form.remarks"
            class="form-control remarks-input"
            placeholder="📝Tips..."
            rows="1"
            @input="autoResize"
          ></textarea>
        </div>

        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading">提交中…</span>
          <span v-else>提交记录</span>
        </button>

        <div v-if="validationError" class="error-message">
          {{ validationError }}
        </div>
      </form>
    </div>
  </div>
</template>




<script>
import axios from 'axios'
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";


export default {
  name: "AddRecord",
  data() {
    return {
        form: {
            date: '',
            amount: 0,
            type: 'income',
            category_id: '',
            remarks: ''
        },
        categories: [],  // 存储类别数据
        loading: false,
        validationError: '',
        sliderStyle: {}  // 滑块样式
    };
  },
  methods: {
    formatAmount() {
    let rawValue = this.formattedAmount.replace(/[^\d.]/g, ""); // 只允许输入正数

    // 确保最多只有一个小数点
    const parts = rawValue.split(".");
    if (parts.length > 2) {
      rawValue = parts[0] + "." + parts.slice(1).join(""); // 只保留一个小数点
    }

    // 限制小数点后最多两位
    if (parts[1] && parts[1].length > 2) {
      rawValue = parts[0] + "." + parts[1].slice(0, 2);
    }

    // **存储正数金额**
    this.form.amount = Math.abs(parseFloat(rawValue)) || 0;

    // **格式化千分位**
    this.formattedAmount = rawValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  },


  async submitRecord() {
    this.validationError = "";
    this.loading = true;

    // **校验金额**
    if (!this.form.amount || this.form.amount <= 0) {
      this.validationError = "金额必须大于零！💰";
      this.loading = false;
      return;
    }

    // **确保类别已选**
    if (!this.form.category_id) {
      this.validationError = "请选择一个类别！📌";
      this.loading = false;
      return;
    }

    // **计算最终金额**
    let processedAmount = this.form.amount;
    if (this.form.type === "expense") {
      processedAmount = -processedAmount; // 只有支出时才转换为负数
    }

    // **提交数据**
    try {
      const response = await axios.post("http://localhost:5002/api/add_record", {
        date: this.form.date,
        amount: processedAmount,
        category_id: this.form.category_id,
        remarks: this.form.remarks
      });

      alert(response.data.message || "提交成功 ✅");

      // **重置表单**
      this.form = { date: "", amount: 0, type: "income", category_id: "", remarks: "" };
      this.formattedAmount = "";
    } catch (error) {
      alert("添加记录失败：" + (error.response ? error.response.data.error : error.message));
    } finally {
      this.loading = false;
    }
  },


  async fetchCategories() {
        try {
            const response = await axios.get('http://localhost:5002/api/get_categories');
            console.log("获取的类别数据:", response.data);

            // 添加类别图标
            const categoryIcons = {
                '餐饮': '🍔',
                '话费': '📱',
                '理发': '💇',
                '交通': '🚴',
                '洗衣': '👔',
                '超市购物': '🏬',
                '零钱': '💰',
                '房租': '🏠'
            };

            // 处理类别数据，确保带有 icon
            this.categories = response.data.map(cat => ({
                ...cat,
                icon: categoryIcons[cat.name] || '📌'
            }));

            // 设置默认类别
            if (this.categories.length > 0) {
                this.selectCategory(this.categories[0].id, 0);
            }

        } catch (error) {
            console.error('获取类别失败：', error);
        }
    },
    selectCategory(id, index) {
        this.form.category_id = id;

        // 获取被选中按钮的 DOM 元素
        this.$nextTick(() => {
            const btn = this.$refs.categoryBtns[index];
            if (btn) {
                this.sliderStyle = {
                    transform: `translateX(${btn.offsetLeft}px)`,
                    width: `${btn.offsetWidth}px`
                };
            }
        });
    }

    
  },
  mounted() {
    this.fetchCategories();
    flatpickr("#date-picker", {
      dateFormat: "Y-m-d",
      defaultDate: this.form.date || new Date(),
      locale: "zh", // 让它支持中文
      onChange: (selectedDates, dateStr) => {
        this.form.date = dateStr;
      }
    });
  }
}
</script>


  
  <style>
  :root {
    --page-bg: #c0bfbf70;           /* 页面背景：橘黄色 */
    --card-bg: #ffffff31;              /* 卡片背景：白色 */
    --card-text: #000000;            /* 卡片文字：深灰 */
    --input-border: #000000;         /* 输入框边框：浅灰 */
    --btn-bg: #6c6b6bc1;            /* 按钮背景：绿色 */
    --btn-hover-bg: #518a5d;      /* 按钮悬停背景：深绿色 */
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  body {
  background: url('/Users/lin/LinZ/Accounting_tool/web_frontend/src/assets/P.jpg') no-repeat center center fixed;
  background-size: cover;
  position: relative;
}
body::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2); /* 轻微暗化背景，提升对比度 */
  z-index: -1;
}

  
  /* 居中容器 */
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }
  
  /* 卡片样式：加宽 card，让 category-bar 有足够空间 */
  .form-card {
  font-family: "Poppins", "Arial", sans-serif; /* 现代感字体 */
  font-size: 16px; /* 默认字体大小 */
  background: rgba(206, 206, 206, 0.704); /* 轻微透明，提高对比度 */
  backdrop-filter: blur(8px); /* 玻璃质感 */
  border-radius: 12px; /* 增加圆角 */
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); /* 更柔和的阴影 */
  width: 100%;
  max-width: 800px;
  text-align: left;
}

  


.card-title {
  font-size: 2rem; /* 标题放大一点 */
  font-weight: 600;
  text-align: center;
  font-family: "STHupo", "Microsoft YaHei", sans-serif; /* 主要使用 STHupo */
  color: #222; /* 让字体颜色更深，增加对比度 */
  letter-spacing: 2px; /* 适当增加字间距，增强质感 */
  animation: fadeIn 1s ease-in-out; /* 淡入动画 */
}



  
  /* 表单组布局 */
  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
  
  /* 标签样式 */
  .form-label {
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
.form-control,
.form-select {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--input-border);
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 1rem;
  transition: all 0.3s ease-in-out;
}

.form-control:hover,
.form-select:hover {
  border-color: var(--btn-bg);
}

.form-control:focus,
.form-select:focus {
  border-color: #6c6b6bc1;
  box-shadow: 0 0 8px rgba(108, 107, 107, 0.5);
}


  
  /* 按钮样式：绿色背景，居中显示 */
  .btn-submit {
    background-color: var(--btn-bg);
    border: none;
    color: #fff;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
    display: block;
    margin: 1rem auto 0;
    transition: background-color 0.3s;
  }


  .toggle-group {
  display: flex;
  border-radius: 8px;
  background: #eee;
  padding: 5px;
}

.toggle-btn {
  flex: 1;
  text-align: center;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  border-radius: 8px;
  transition: all 0.3s;
}

input:checked + .toggle-btn {
  background: var(--btn-bg);
  color: white;
}


  /* 新增：错误提示样式 */
    .error-message {
    color: #984c4a;  /* 红色 */
    margin-bottom: 1rem;
    text-align: center;
    font-weight: bold;
    }
  
  .btn-submit:hover {
    background-color: var(--btn-hover-bg);
  }


/* 让 category-bar 适配 form-card 宽度 */
.category-bar {
  width: 100%; /* 让其宽度和 form-card 一致 */
  overflow-x: auto; /* 启用横向滚动 */
  white-space: nowrap;
  border-radius: 6px;
  background: #eee;
  padding: 4px; /* 适当增加 padding */
  position: relative;
  display: flex;
  justify-content: center;
}

/* 滑动轨道 */
.category-track {
  display: flex;
  position: relative;
  gap: 6px; /* 适当间距 */
  width: 100%;
  justify-content: space-between; /* 让按钮均匀分布 */
}

/* 单个类别按钮 */
.category-btn {
  flex: 1; /* 让按钮自适应宽度 */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 6px 10px; /* 适当大小 */
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem; /* 适中字体 */
  transition: all 0.3s ease-in-out;
  white-space: nowrap;
  background: transparent;
  position: relative;
  z-index: 2;
}

/* 滑块动画 */
.category-slider {
  position: absolute;
  height: 100%;
  background: var(--btn-bg);
  border-radius: 6px;
  transition: transform 0.3s ease-in-out, width 0.3s ease-in-out;
  z-index: 1;
}

/* 选中状态 */
.category-btn.active {
  color: white;
}

/* 图标 */
.icon {
  font-size: 1rem; /* 适中图标 */
}

/* 文字 */
.text {
  font-size: 0.75rem; /* 适中字体 */
  font-weight: bold;
}





.amount-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}
/* 💰 图标 */
.amount-icon {
  position: absolute;
  left: 12px;
  font-size: 1.2rem;
  color: #888;
  pointer-events: none; /* 避免影响输入框点击 */
}

/* 金额输入框 */
.amount-input {
  width: 100%;
  padding-left: 40px; /* 避免文字覆盖货币符号 */
  font-size: 1.2rem;
  font-weight: bold;
  text-align: left;
  border-radius: 8px;
  border: 1px solid #ccc;
  transition: all 0.3s ease-in-out;
}

/* 输入框获得焦点时 */
.amount-input:focus {
  border-color: #6c6b6bc1;
  box-shadow: 0 0 8px rgba(108, 107, 107, 0.5);
}



/* 日期选择器容器 */
.date-picker-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

/* 📅 图标 */
.date-icon {
  position: absolute;
  left: 12px;
  font-size: 1.2rem;
  color: #888;
  pointer-events: none; /* 避免影响输入框点击 */
}

/* 日期输入框 */
.form-control {
  width: 100%;
  padding: 10px 12px;
  padding-left: 40px; /* 给左侧图标留空间 */
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid var(--input-border);
  background: #fff;
  transition: all 0.3s ease-in-out;
}

/* 输入框获得焦点时 */
.form-control:focus {
  border-color: var(--btn-bg);
  box-shadow: 0 0 8px rgba(108, 107, 107, 0.5);
}




/* 让备注输入框更美观 */
.remarks-input {
  width: 97%;
  font-size: 1rem;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid var(--input-border);
  background: #fff;
  transition: all 0.3s ease-in-out;
  resize: none; /* 禁止手动调整大小 */
  min-height: 40px; /* 设置最小高度 */
  max-height: 150px; /* 限制最大高度，避免过大 */
  overflow-y: auto; /* 超出时可滚动 */
}

/* 输入框获得焦点时 */
.remarks-input:focus {
  border-color: var(--btn-bg);
  box-shadow: 0 0 8px rgba(108, 107, 107, 0.5);
}







  </style>