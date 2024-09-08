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
            <input type="text" v-model="resourceName" placeholder="内容" />
            <select v-model="selectedSubject">
              <option value="全部">科目</option>
              <option value="计算机">计算机</option>
              <option value="数学">数学</option>
            </select>
            <select v-model="selectedUploadTime">
              <option value="全部">上传时间</option>
              <option value="2024-08-20">2024-08-20</option>
            </select>
  
            <button @click="searchResources">查询</button>
            <button @click="resetFields">清空</button>

          </div>
  
          <table class="resource-table">
            <thead>
              <tr>
                <th>选择</th>
                <th>序号</th>
                <th>资料内容</th>
                <th>上传人</th>
                <th>学科分类</th>
                <th>上传时间</th>
                <th>截止时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(resource, index) in resources" :key="index">
                <td>
                  <input type="checkbox" v-model="resource.selected" />
                </td>
                <td>{{ index + 1 }}</td>
                <td>{{ resource.name }}</td>
                <td>{{ resource.uploader }}</td>
                <td>{{ resource.subject }}</td>
                <td>{{ resource.uploadTime }}</td>
                <td>{{ resource.deadline }}</td>
                <td>
                  <button @click="viewResource(resource)">查看</button>
                  <button @click="downloadResource(resource)">下载</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="pagination">
            <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
            <span>第 {{ currentPage }} 页</span>
            <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
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
        resourceName: '',
        selectedSubject: '全部',
        selectedUploadTime: '全部',
        resources: [
          // 添加更多示例资源以便于分页
          { name: 'C++资料1', uploader: '张三', subject: '计算机', uploadTime: '2024-08-20', deadline: '2024-08-25', selected: false },
          { name: 'Python资料1', uploader: '李四', subject: '计算机', uploadTime: '2024-08-21', deadline: '2024-08-26', selected: false },
          { name: '数学资料1', uploader: '王五', subject: '数学', uploadTime: '2024-08-22', deadline: '2024-08-27', selected: false },
          { name: '英语资料1', uploader: '赵六', subject: '英语', uploadTime: '2024-08-23', deadline: '2024-08-28', selected: false },
          { name: '物理资料1', uploader: '钱七', subject: '物理', uploadTime: '2024-08-24', deadline: '2024-08-29', selected: false },
          { name: '化学资料1', uploader: '孙八', subject: '化学', uploadTime: '2024-08-25', deadline: '2024-08-30', selected: false },
          // 更多资源...
        ],
        currentPage: 1,
        itemsPerPage: 5, // 每页显示的条数
      };
    },
    methods: {
      logout() {
        // 退出登录逻辑
        alert('已退出登录');
        this.$router.push('/');
      },
      searchResources() {
        // 查询逻辑
        alert('查询功能尚未实现');
      },
      resetFields() {
        this.resourceName = '';
        this.selectedSubject = '全部';
        this.selectedUploadTime = '全部';
        this.$refs.uploadFile.value = ''; // 清空文件选择
      },
      uploadFile() {
        const fileInput = this.$refs.uploadFile;
        if (!fileInput.files.length) {
          alert('请先选择文件进行上传');
        } else {
          alert('文件上传功能尚未实现');
        }
      },
      viewResource(resource) {
        // 查看资源逻辑
        alert(`查看: ${resource.name}`);
      },
      downloadResource(resource) {
        // 下载资源逻辑
        alert(`下载: ${resource.name}`);
      },
    },
  };
  </script>
  
  <style scoped>
  /* =========================
     通用样式
  ========================= */
  * {
    box-sizing: border-box; /* 使用边框盒模型 */
    margin: 0;
    padding: 0;
  }
  
  html, body {
    height: 100%; /* 确保 html 和 body 高度为 100% */
    margin: 0;
    font-family: 'Arial', sans-serif; /* 设置字体 */
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
    margin-left: 20px; /* 主内容与侧边栏有间距 */
    overflow: auto; /* 允许滚动 */
  }
  
  .user-controls {
    display: flex;
    align-items: center; /* 垂直居中对齐 */
  }
  
  .user-controls span {
    margin-right: 20px; /* 添加右边距以分隔元素 */
  }
  
  .welcome-message {
    margin-left: 10px;
    margin-right: 20px; /* 与选择器分开 */
    font-size: 0.9em; /* 调整字体大小 */
    color: #34495e; /* 设置颜色 */
  }
  
  .header {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 20px;
  }
  
  /* =========================
     内容区域样式
  ========================= */
  .content-area {
    display: flex;
    flex-direction: column;
    flex: 1; /* 填满剩余空间 */
  }
  
  /* =========================
     搜索栏样式
  ========================= */
  .search-bar {
    display: flex;
    align-items: center;
    margin-bottom: 20px; /* 添加底部边距 */
  }
  
  .search-bar input,
  .search-bar select {
    margin-right: 10px; /* 添加右边距 */
  }
  
  /* =========================
     表格样式
  ========================= */
  .resource-table {
    width: 100%;
    max-height: 400px; /* 最大高度 */
    border-collapse: collapse; /* 合并边框 */
    overflow-y: auto; /* 允许竖向滚动 */
    font-size: 14px; /* 表格字体大小 */
    margin-bottom: 20px; /* 表格底部间距 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 盒子阴影 */
    border-radius: 5px; /* 圆角 */
  }
  
  .resource-table th,
  .resource-table td {
    border: 1px solid #ddd; /* 添加边框 */
    padding: 8px; /* 添加内边距 */
    text-align: center; /* 内容居中 */
  }
  
  .resource-table th {
    background-color: #f2f2f2; /* 表头背景颜色 */
  }
  
  .resource-table tr:hover {
    background-color: #f1f1f1; /* 鼠标悬停时行背景颜色 */
  }
  
  /* =========================
     下拉框和输入框样式
  ========================= */
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