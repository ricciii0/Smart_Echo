<template>
  <div class="login-page">
    <div class="container">
      <img src="../../../public/img/seu_logo.png" alt="Southeast University Logo" class="logo" />
      <h1>智慧教学系统</h1>
      <form @submit.prevent="handleSubmit">
        <input type="text" v-model="username" placeholder="请输入账号" required />
        <input type="password" v-model="password" placeholder="请输入密码" required />
        <div class="checkbox">
          <input type="checkbox" v-model="remember" id="remember" />
          <label for="remember">记住密码</label>
        </div>
        <button type="submit" class="btn">登录</button>
        <div class="link" @click="$router.push('/forgot-password')">忘记密码?</div>
        <div class="link">
          <router-link to="/register">没有账号？点击注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex"; // 引入 Vuex 的 mapActions

export default {
  data() {
    return {
      username: '',
      password: '',
      remember: false,
    };
  },
  methods: {
    ...mapActions(['login']),  // 映射 Vuex 的 login action

    async handleSubmit() {
      try {
        // 发送POST请求到后端
        const response = await axios.post('http://127.0.0.1:5000/auth/login/', {
          user_id: this.username,
          password: this.password,
          remember: this.remember,
        });

        // 根据后端响应处理登录结果
        if (response.data.success) {
          // 调用 Vuex 的 login action，并传递用户类型
          await this.login({
            user_type: response.data.user_type,
          });

          // 登录成功后跳转到主页面
          this.$router.push('/main');
        } else {
          alert('登录失败，请检查用户名和密码');
        }
      } catch (error) {
        console.error('登录请求失败:', error);
        alert('登录请求失败，请稍后再试');
      }
    },
  },
};
</script>


<style scoped>
/* 全局样式 */
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

.login-page {
  height: 100vh; /* 视口高度 */
  background: url('../../../public/img/background.png') no-repeat center center fixed; /* 背景图 */
  background-size: cover; /* 背景图覆盖 */
  display: flex; /* 使用 flexbox 居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.container {
  background: rgba(255, 255, 255, 0.95); /* 半透明白色背景 */
  border-radius: 15px; /* 圆角 */
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); /* 更柔和的阴影 */
  padding: 40px;
  width: 400px;
  text-align: center;
}

.logo {
  width: 100px; /* 调整 logo 大小 */
  margin-bottom: 20px; /* logo 与其他元素之间的间距 */
}

h1 {
  color: #333; /* 标题颜色 */
  margin-bottom: 20px; /* 标题与表单间距 */
  font-size: 24px; /* 标题大小 */
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px; /* 增加内边距 */
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s; /* 添加过渡效果 */
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #5c6bc0; /* 聚焦时边框颜色 */
  outline: none; /* 去掉默认的聚焦轮廓 */
}

.btn {
  width: 100%; /* 按钮宽度 */
  padding: 12px;
  margin-top: 10px;
  background-color: #5c6bc0; /* 按钮颜色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s; /* 添加过渡效果 */
}

.btn:hover {
  background-color: #4a5cb8; /* 悬停时按钮颜色 */
}

.link {
  margin-top: 10px; /* 上边距 */
  font-size: 14px;
}

.link a {
  color: #5c6bc0; /* 链接颜色 */
  text-decoration: none; /* 去掉下划线 */
}

.link a:hover {
  text-decoration: underline; /* 悬停时添加下划线 */
}
</style>