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
            <div class="grading-area">
          <h3>机器批改</h3>
          <div class="file-selection">
            <select v-model="selectedFile" @change="fetchFileInfo">
              <option disabled value="">请选择文件</option>
              <option v-for="file in files" :key="file.id" :value="file.id">
                {{ file.name }}
              </option>
            </select>
            <button @click="submitForGrading">提交批改</button>
          </div>
          <div v-if="fileInfo">
            <p>学生姓名: {{ fileInfo.studentName }}</p>
            <p>提交日期: {{ fileInfo.submitDate }}</p>
            <p>得分: {{ gradingResult ? gradingResult.score : '尚未批改' }}</p>
            <p>反馈: {{ gradingResult ? gradingResult.feedback : '尚未批改' }}</p>
            <button v-if="gradingResult" @click="downloadReport">下载报告</button>    </div>
        </div>

        <div class="manual-grading-area">
          <h3>手动批改</h3>
          <div class="manual-scoring">
            <label for="manualScore">评分:</label>
            <input type="number" v-model="manualScore" min="0" max="100" />
          </div>
          <div class="reply-area">
            <label for="teacherReply">教师回复:</label>
            <textarea v-model="teacherReply" placeholder="输入反馈..."></textarea>
          </div>
          <button @click="submitManualGrading">提交手动批改</button>
        </div>
        <div class="progress-section">
          <h3>批改进度列表</h3>
          <ul>
            <li v-for="(file, index) in files" :key="file.id">
              {{ file.name }} - 状态: {{ gradingResults[index]?.status || '未批改' }}
            </li>
          </ul>

          <h3>分数分布统计</h3>
          <div class="score-distribution">
            <canvas id="scoreChart"></canvas>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>
  
  <script>
      import Sidebar from '../shared/Sidebar.vue';
      import UserControls from '../shared/UserControls.vue';
      import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
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
        files: [ { id: 1, name: '练习题1 - 学生A' },
        { id: 2, name: '练习题2 - 学生B' },
        { id: 3, name: '练习题3 - 学生C' },], // 用于存储文件列表
      selectedFile: '',
      fileInfo: null, // 存储所选文件的学生信息
      gradingResult: null,
      manualScore: '',
      teacherReply: '',
      gradingResults: [] // 用于存储批改结果
      };
    },
    methods: {
        async fetchFiles() {
      // 从后端获取文件列表
      try {
        const response = await axios.get('YOUR_BACKEND_API_URL/files');
        this.files = response.data; // 假设返回的数据格式为[{ id: 1, name: '文件1' }, ...]
      } catch (error) {
        console.error('获取文件列表失败:', error);
      }
    },
    fetchFileInfo() {
      // 根据选择的文件模拟获取学生信息和提交日期
      const fileDetails = {
        1: { studentName: '学生A', submitDate: '2023-09-01' },
        2: { studentName: '学生B', submitDate: '2023-09-02' },
        3: { studentName: '学生C', submitDate: '2023-09-03' },
      };
      this.fileInfo = fileDetails[this.selectedFile] || null;
    },
    submitForGrading() {
         // 模拟机器批改的结果
         this.gradingResults[this.selectedFile - 1] = {
        score: this.gradingResult.score,
        status: '已批改'
      };

      alert('提交批改请求');
      this.updateScoreChart(); // 更新图表
    },
    downloadReport() {
      // 下载批改结果的报告
      alert('下载报告');
    },
    submitManualGrading() {
      // 提交手动评分和回复
      alert(`评分: ${this.manualScore}, 回复: ${this.teacherReply}`);
    },
    updateScoreChart() {
      const ctx = document.getElementById('scoreChart').getContext('2d');
      const scores = this.gradingResults.map(result => result?.score || 0);
      const labels = this.files.map(file => file.name);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: '分数分布',
            data: scores,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  },

  mounted() {
    this.fetchFiles(); // 组件挂载时获取文件列表
    this.updateScoreChart(); // 初始化图表
  
  },
  };
  </script>
  
  <style scoped>
  .grading-area, .manual-grading-area {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}
.progress-section {
  margin-top: 30px;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.score-distribution {
  margin-top: 20px;
}
.upload-area {
  margin-bottom: 20px;
}

.manual-scoring, .reply-area {
  margin-bottom: 15px;
}
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