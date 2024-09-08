<template>
  <header class="header">
    <div class="user-controls">
      <span>
        <select v-model="selectedClass">
          <option v-for="classItem in classList" :key="classItem">{{ classItem }}</option>
        </select>
      </span>
      <span class="welcome-message">欢迎您，{{ username }}</span>
      <button @click="logout">退出登录</button>
    </div>
  </header>
</template>

<script>
import axios from 'axios'; 

export default {
  name: 'UserControls',
  data() {
    return {
      username: '张三', // 示例用户名
      selectedClass: '',
      classList: [], // 用于存储班级列表
    };
  },
  mounted() {
    this.fetchClassList(); // 组件挂载后获取班级列表
  },
  methods: {
    fetchClassList() {
      axios.get('/api/classes') // 替换为实际的 API 路径
        .then(response => {
          this.classList = response.data; // 假设返回的数据是班级数组
          if (this.classList.length > 0) {
            this.selectedClass = this.classList[0]; // 默认选择第一个班级
          }
        })
        .catch(error => {
          console.error('获取班级列表失败:', error);
        });
    },
    logout() {
      this.$emit('logout'); // 触发 logout 事件
	  this.$router.push('/');
    },
  },
};
</script>

<style>
.user-controls {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
}

.user-controls span {
  margin-right: 20px; /* 添加右边距以分隔元素 */
}

.welcome-message {
  margin-left: 10px;
  margin-right: 20px; /* 添加右边距以与选择器分开 */
  font-size: 0.9em; /* 调整字体大小 */
  color: #34495e; /* 设置颜色 */
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
}

select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ced4da;
  background-color: #fff;
  color: #495057;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

select:hover {
  border-color: #80bdff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

button {
  padding: 8px 10px;
  border-radius: 5px;
  border: none;
  background: rgb(255, 255, 255);
  color: black;
  font-weight: bold;
  font-size: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 10px;
}
</style>