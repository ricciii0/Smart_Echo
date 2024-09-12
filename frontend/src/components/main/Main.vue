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
          <div class="photo-track">
            <!-- 双倍循环图片，实现无缝滚动 -->
            <div class="photo-container" v-for="(photo, index) in doublePhotos" :key="index">
              <img :src="photo.src" :alt="photo.alt" class="photo-item" />
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
        username: 'admin', // 根据实际用户名进行设置
        selectedClass: '班级1',
        announcements: [
          "公告1：请注意课程安排。",
          "公告2：新学期开始，欢迎大家回到学校！",
          "公告3：请参加下周的家长会。",
          "公告4：新课程即将上线，敬请期待！",
        ],
        photos: [
          { src: '/img/1.jpg', alt: '照片1' }, // 使用绝对路径引用 public 文件夹中的图片
          { src: '/img/2.jpg', alt: '照片2' },
          { src: '/img/3.jpg', alt: '照片3' },
          { src: '/img/4.jpg', alt: '照片4' },
          { src: '/img/5.jpg', alt: '照片5' },
          { src: '/img/6.jpg', alt: '照片6' },
          { src: '/img/7.jpg', alt: '照片7' },
          { src: '/img/8.jpg', alt: '照片8' },
          { src: '/img/9.jpg', alt: '照片9' },
            ],
      };
    },
    computed: {
      // 将照片数组加倍以实现无缝滚动
      doublePhotos() {
        return [...this.photos, ...this.photos];
      }
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
  background-image: url('../../../public/img/background.png');
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

.content-area {
  display: flex;
  flex: 1; /* 使内容区域填满剩余空间 */
}

.announcement-board {
  flex: 1;
  width: 50%; /* 公告栏占据左半部分 */
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

/* 照片墙部分样式 */
.photo-wall {
  flex: 1;
  width: 50%; /* 照片墙占据右半部分 */
  position: relative;
  overflow: hidden; /* 只在照片墙区域内滚动 */
}

.photo-wall h2 {
  margin-bottom: 10px; /* 增加标题与内容之间的间距 */
}

.photo-track {
  display: flex;
  width: max-content;
  animation: slide 30s linear infinite; /* 滚动动画 */
}

.photo-container {
  flex-shrink: 0; /* 防止图片收缩 */
  width: 100px;
  margin-right: 10px;
}

img {
  width: 100%; /* 照片按照原始比例缩放 */
  height: auto;
}

@keyframes slide {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%); /* 控制滚动范围，使其循环滚动 */
  }
}
</style>


