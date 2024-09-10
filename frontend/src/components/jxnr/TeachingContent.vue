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
          <input type="text" v-model="resourceName" placeholder="讲义名称" />
<!--          <select v-model="selectedUploadTime">-->
<!--            <option value="全部">上传时间</option>-->
<!--            <option value="2024-08-20">2024-08-20</option>-->
<!--            -->
<!--          </select>-->
          <!-- 日期选择器 -->
          <input type="date" v-model="selectedUploadTime" placeholder="选择上传时间" />
          <button @click="searchResources">查询</button>
                    <input type="file" ref="uploadFile" />
          <button @click="uploadFile">上传</button>
        </div>

        <table class="resource-table">
          <thead>
            <tr>
              <th>选择</th>
              <th>序号</th>
              <th>讲义名称</th>
              <th>上传时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(resource, index) in resources" :key="index">
              <td>
                <input type="checkbox" v-model="resource.selected" />
              </td>
              <td>{{ index + 1 }}</td>
              <td>{{ resource.filename }}</td>
              <td>{{ resource.uploadTime }}</td>
              <td>
                <button @click="viewResource(resource.id)">查看</button>
                <button @click="downloadResource(resource.id)">下载</button>
              </td>
            </tr>
          </tbody>
        </table>
        <resource-detail
    v-if="showDetail"
    :resource="selectedResource"
    @close="closeDetail"
  />

		        <div class="pagination">
		          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
		          <span>第 {{ currentPage }} 页</span>
		          <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
		        </div>

        <div class="action-buttons">
          <button @click="deleteSelected">删除</button>
          <button @click="previewSelected">预览</button>
          <button @click="downloadSelected">下载</button>
          <select v-model="generatedFileType">
            <option value="全部">生成文件类型</option>
            <option value=".txt">.txt</option>
            <option value=".doc">.doc</option>
            <option value=".pdf">.pdf</option>
          </select>
          <button @click="generateFiles">智能生成</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
	import Sidebar from '../shared/Sidebar.vue';
	import UserControls from '../shared/UserControls.vue';
  import axios from "axios";
  import Detail from '../shared/Detail.vue';
	export default {
		  name: 'OnlineExercise',
		  components: {
		    Sidebar,
			UserControls,
		  },
  // data() {
  //     return {
  //
  //       username: 'admin',
  //       selectedClass: '班级1',
  //       resourceName: '',
  //       selectedUploadTime: '全部',
  //       generatedFileType: '全部',
  //       resources: [
  //         { name: 'C++讲义1', uploadTime: '2024-08-20', selected: false },
  //         { name: 'Python讲义1', uploadTime: '2024-08-20', selected: false },
  //         // 更多数据行...
  //       ],
  //       showDetail: false,
  //       selectedResource: null,
  //       currentPage: 1,
  //       itemsPerPage: 5, // 每页显示的条数
  //     };
  //   },
    data() {
    return {
      resourceName: '',  // 用户输入的讲义名称
      selectedUploadTime: '',  // 用户选择的上传时间
      resources: []  // 查询结果将存储在这里
    };
  },


    computed: {
      totalPages() {
        return Math.ceil(this.resources.length / this.itemsPerPage);
      },
      paginatedResources() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.resources.slice(start, start + this.itemsPerPage);
      },
    },
  methods: {
  //   viewResource(resource) {
  //   this.selectedResource = resource;
  //   this.showDetail = true;
  // },

    viewResource(fileId) {
    // 打开新窗口预览文件
    window.open(`http://127.0.0.1:5000/preview_material/${fileId}`, '_blank');
    },

    downloadResource(fileId) {
    // 打开新窗口下载文件
    window.open(`http://127.0.0.1:5000/download_material/${fileId}`, '_blank');
   },
  closeDetail() {
    this.showDetail = false;
    this.selectedResource = null;
  },    logout() {
      // 退出登录逻辑
      alert('已退出登录');
      this.$router.push('/');
    },
    // searchResources() {
    //   // 查询逻辑
    //   alert('查询功能尚未实现');
    // },


    //上传文件
    async uploadFile() {
    // 获取用户选择的文件
    const file = this.$refs.uploadFile.files[0];
    if (!file) {
      alert('请先选择文件');
      return;
    }

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('file', file);  // 文件
    formData.append('subject', this.resourceName);  // 讲义名称（假设与文件名一起上传）

    try {
      // 发送 POST 请求到后端
      const response = await axios.post('http://127.0.0.1:5000/upload_material', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert(response.data.message);  // 提示上传结果
    } catch (error) {
      console.error('上传失败:', error);
      alert('文件上传失败，请重试');
    }
  },

    async searchResources() {
      try {
        // 发送查询请求到后端
        const response = await axios.get('http://127.0.0.1:5000/search_material', {
          params: {
            filename: this.resourceName,
            date: this.selectedUploadTime  // 日期自动格式化为 'YYYY-MM-DD'
          }
        });
        // 将后端返回的文件列表存储到 resources 数组中
        this.resources = response.data;
      } catch (error) {
        console.error('查询时出错:', error);
        alert('查询失败，请检查您的查询条件或重试。');
      }
    },

	    changePage(page) {
	      if (page > 0 && page <= this.totalPages) {
	        this.currentPage = page;
	      }
	    },
    // deleteSelected() {
    //   // 删除选中的资源逻辑
    //   alert('删除功能尚未实现');
    // },

    async deleteSelected() {
    // 过滤出选中的资源
    const selectedResources = this.resources.filter(resource => resource.selected);
    if (selectedResources.length === 0) {
      alert('请选择要删除的文件');
      return;
    }

    // 遍历选中的资源，逐个删除
    try {
      for (const resource of selectedResources) {
        await axios.delete(`http://127.0.0.1:5000/delete_material/${resource.id}`);
        // 从前端列表中删除
        this.resources = this.resources.filter(r => r.id !== resource.id);
      }
      alert('选中的文件已删除');
    } catch (error) {
      console.error('删除文件时出错:', error);
      alert('删除文件失败，请重试。');
    }
    },
    // previewSelected() {
    //   // 预览选中的资源逻辑
    //   alert('预览功能尚未实现');
    // },

    previewSelected() {
    // 假设你有一个 selectedResources 数组存储了选中的资源
    const selectedResources = this.resources.filter(resource => resource.selected);
    if (selectedResources.length !== 1) {
      alert('请只选择一个文件进行预览');
      return;
    }

    // 获取选中的文件，并在新窗口中打开以预览
    const resource = selectedResources[0];
    window.open(`http://127.0.0.1:5000/preview_material/${resource.id}`, '_blank');
    },
    // downloadSelected() {
    //   // 下载选中的资源逻辑
    //   alert('下载功能尚未实现');
    // },
    downloadSelected() {
    // 假设你有一个 selectedResources 数组存储了选中的资源
    const selectedResources = this.resources.filter(resource => resource.selected);
    if (selectedResources.length === 0) {
      alert('请选择要下载的文件');
      return;
    }

    // 遍历选中的资源，逐个下载
    selectedResources.forEach(resource => {
      window.open(`http://127.0.0.1:5000/download_material/${resource.id}`, '_blank');
    });
    },
    generateFiles() {
      // 智能生成逻辑
      alert('智能生成功能尚未实现');
    },

    // downloadResource(resource) {
    //   // 下载资源逻辑
    //   alert(`下载: ${resource.name}`);
    // },
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
  margin-left: 5px;
  margin-right: 5px;
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
  margin-right: 5px; /* 按钮间距 */
  margin-left: 5px;
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

.action-buttons {
  display: flex;
  
  margin-top: 20px; /* 添加顶部间距 */
  margin-top: auto;
}
</style>