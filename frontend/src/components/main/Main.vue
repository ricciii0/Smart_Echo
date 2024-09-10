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
        <div class="announcement-board">
          <h2>公告栏</h2>
          <ul>
            <li v-for="(announcement, index) in announcements" :key="index" class="announcement-item">
              {{ announcement }}
            </li>
          </ul>
        </div>
        
        <div class="photo-wall">
          <h2>照片墙</h2>
          <div class="photos">
             <img v-for="(photo, index) in photos" :key="index" :src="photo.src" :alt="photo.alt" class="photo-item" /> </div>
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
      username: 'admin', // 根据实际用户名进行设置
      selectedClass: '班级1',
      announcements: [
        "公告1：请注意课程安排。",
        "公告2：新学期开始，欢迎大家回到学校！",
        "公告3：请参加下周的家长会。",
        "公告4：新课程即将上线，敬请期待！",
      ],
      photos: [
        { src: '../../img/photo1.jpg', alt: '照片1' },
        { src: '../../img/photo2.jpg', alt: '照片2' },
        { src: '../../img/photo3.jpg', alt: '照片3' },
        { src: '../../img/photo4.jpg', alt: '照片4' },
        { src: '../../img/photo5.jpg', alt: '照片5' },
      ],
    };
  },
  methods: {
    handleLogout() {
      // 退出登录逻辑
      alert('已退出登录');
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
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

.main-container {
  display: flex;
  background-image: url('../../img/background.png');
  background-size: cover; /* 使图片覆盖整个容器 */
  background-position: center; /* 图片居中 */
  background-repeat: no-repeat; /* 不重复背景图片 */
  height: 100vh; /* 填满整个视口高度 */
  margin: 0;
}



.main-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  margin-left: 20px; /* 确保主内容与侧边栏有间距 */
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

.content-area {
  display: flex;
  flex: 1; /* 使内容区域填满剩余空间 */
}

.announcement-board {
  flex: 1;
  margin-right: 30px; /* 与右侧的照片墙隔开 */
  padding: 15px; /* 添加内边距 */
  border-radius: 5px; /* 圆角效果 */
  min-width: 300px; /* 设置最小宽度 */
  overflow: auto; /* 允许滚动 */
}

.announcement-board h2 {
  margin-bottom: 10px; /* 增加标题与内容之间的间距 */
}

.announcement-item {
  background: rgba(255, 255, 255, 0.3); /* 设置为半透明的浅灰色 */
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px; /* 每条公告之间的间距 */
}

.photo-wall {
  flex: 1;
}

.photo-wall h2 {
  margin-bottom: 10px; /* 增加标题与内容之间的间距 */
}

.photos {
  display: flex;
  overflow-x: auto; /* 允许横向滚动 */
  padding-bottom: 10px; /* 底部内边距 */
}

.photos img {
  width: 100px;
  height: 100px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer; /* 鼠标变成手形，表示可点击 */
}

/*下拉框的样式*/

select,
input[type="text"],
input[type="file"] {
  padding: 10px;
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
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  background:rgb(255, 255, 255) ;
  color: black;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
 
  margin-right: 10px;
}





.resource-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.resource-table th,
.resource-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.resource-table th {
  background-color: rgba(255, 255, 255, 0.5);
  color: #001a33;
  font-weight: bold;
}

.resource-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.resource-table tbody tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.resource-table tbody td {
  border-right: 1px solid #ddd;
}

.resource-table tbody td:last-child {
  border-right: none;
}
</style>