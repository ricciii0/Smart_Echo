<template>
  <div class="main-container">
<Sidebar />
  <router-view />

    <div class="main-content">
      <UserControls 
            :username="username" 
            v-model="selectedClass" 
            @logout="handleLogout" 
          />

      <div class="content-area">
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="关键词" />
          <button @click="searchResources">查询</button>
        </div>

        <div class="flex-container">
          <div class="history">
            <h3>历史记录</h3>
            <div class="history-item">
              <button @click="viewContent('题目内容1')">题目内容1</button>
            </div>
            <div class="history-item">
              <button @click="viewContent('题目内容2')">题目内容2</button>
            </div>
            <div class="history-item">
              <button @click="viewContent('题目内容3')">题目内容3</button>
            </div>
          </div>

          <div class="chat-container">
            <div class="question-content">
              <div class="message" v-for="(msg, index) in messages" :key="index">
                <div class="message-bubble" :class="{ 'user-message': msg.type === 'user', 'bot-message': msg.type === 'bot' }">
                  <p>{{ msg.text }}</p>
                </div>
              </div>
            </div>

            <div class="input-area">
              <input type="text" v-model="userMessage" placeholder="输入问题..." />
              <button @click="sendMessage">发送</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
	import Sidebar from '../shared/Sidebar.vue';
	import UserControls from '../shared/UserControls.vue';
	export default {
		  name: 'OnlineExercise',
		  components: {
		    Sidebar,
			UserControls,
		  },
  data() {
    return {
      username: 'admin',
      selectedClass: '班级1',
      searchQuery: '',
      userMessage: '',
      messages: [],
    };
  },
  methods: {
    logout() {
      alert('已退出登录');
      this.$router.push('/');
    },
    searchResources() {
      alert('查询功能尚未实现');
    },
    viewContent(content) {
      alert(`查看内容: ${content}`);
    },
    async sendMessage() {
      if (!this.userMessage) return;

      // 添加用户消息到对话框
      this.messages.push({ text: this.userMessage, type: 'user' });

      // 调用后端API
      try {
        const response = await axios.post('YOUR_BACKEND_API_URL', {
          question: this.userMessage,
        });
        // 假设后端返回的回答在 response.data.answer
        this.messages.push({ text: response.data.answer, type: 'bot' });
      } catch (error) {
        console.error('Error fetching response:', error);
        this.messages.push({ text: '无法获取回答，请稍后再试。', type: 'bot' });
      }

      // 清空输入框
      this.userMessage = '';
    },
  },
};
</script>

<style scoped>
/* =========================
   通用样式
========================= */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  margin: 0;
  font-family: 'Arial', sans-serif;
}

/* =========================
   主容器样式
========================= */
.main-container {
  display: flex;
  background-image: url('../../img/background.png');
  background-size: cover; /* 使图片覆盖整个容器 */
  background-position: center; /* 图片居中 */
  background-repeat: no-repeat; /* 不重复背景图片 */
  height: 100vh; /* 填满整个视口高度 */
  margin: 0;
}

/* =========================
   主内容样式
========================= */
.main-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  margin-left: 20px;
  overflow: auto;
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
}

.user-controls {
  display: flex;
  align-items: center;
}

.user-controls span {
  margin-right: 20px;
}

.welcome-message {
  margin-left: 10px;
  margin-right: 20px;
  font-size: 0.9em;
  color: #34495e;
}

/* =========================
   内容区域样式
========================= */
.content-area {
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* =========================
   搜索栏样式
========================= */
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar input,
.search-bar select {
  margin-right: 10px;
}

/* =========================
   聊天区域样式
========================= */
.flex-container {
  display: flex;
  gap: 20px;
  flex: 1;
}

.history {
  flex: 1;
  max-width: 150px;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  overflow-y: auto;
  max-height: 600px;
}

.chat-container {
  flex: 3;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.question-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.input-area {
  display: flex;
  margin-top: 10px;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.input-area button {
  padding: 10px 15px;
  margin-left: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.input-area button:hover {
  background-color: #0056b3;
}

/* =========================
   消息样式
========================= */
.message {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 10px;
}

.message-bubble {
  background-color: #e1ffc7;
  border-radius: 10px;
  padding: 10px;
  max-width: 80%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.user-message {
  background-color: #cfe2ff;
  align-self: flex-end;
}

.bot-message {
  background-color: #e1ffc7;
}

/* =========================
   历史记录样式
========================= */
.history-item {
  margin: 15px 0;
}



select,
input[type="text"],
input[type="file"] {
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

/* =========================
   按钮样式
========================= */
button {
  padding: 8px 10px;
  border-radius: 5px;
  border: none;
  background: rgb(255, 255, 255);
  color: black;
  font-weight: bold;
  font-size: 12px; /* 调整字体大小 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 10px; /* 按钮间距 */
}


.pagination {
  display: flex;
  justify-content: center;
    align-items: center; /* 确保按钮和文本垂直居中 */
  margin: 20px 0; /* 添加上下间距 */
 font-size: 12px; /* 调整字体大小 */
}

.pagination button {
  padding: 4px 8px; /* 调整内边距 */
  font-size: 12px; /* 调整字体大小 */
  margin: 0 20px; /* 调整按钮间距 */
  border-radius: 3px; /* 圆角效果 */
  background-color: #f0f0f0; /* 背景颜色 */
  cursor: pointer; /* 鼠标悬停效果 */
  transition: background-color 0.3s; /* 平滑过渡 */
}

.pagination button:hover {
  background-color: #e0e0e0; /* 鼠标悬停效果 */
}

.pagination button:disabled {
  background-color: #ccc; /* 禁用状态背景颜色 */
  cursor: not-allowed; /* 禁用状态光标 */
}
</style>