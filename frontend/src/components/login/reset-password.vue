<template>
  <div class="reset-password-page">
    <div class="reset-password-container">
      <h1>重置密码</h1>
      <p>请填写您的新密码：</p>

      <!-- 新密码输入框 -->
      <input
        type="password"
        v-model="newPassword"
        placeholder="请输入新密码"
        required
      />

      <!-- 确认密码输入框 -->
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="确认新密码"
        required
      />

      <!-- 提交按钮 -->
      <button @click="resetPassword">确定</button>

      <!-- 返回登录 -->
      <div class="link" @click="$router.push('/')">返回登录</div>
          <router-link
        v-if="isPasswordReset"
        to="/main"
        class="link-btn"
      >
        密码重置成功，返回登录
      </router-link>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      isPasswordReset: false, // 用于跟踪密码是否成功重置
    };
  },
  methods: {
    async resetPassword() {
  if (this.newPassword === this.confirmPassword) {
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/forgot/reset/', {
        password: this.newPassword
      });
      if (response.status === 200) {
        alert('密码重置成功');
        this.$router.push('/'); // 重置密码成功后，跳转回登录页面
      } else {
        alert('重置密码失败，请稍后再试。');
      }
    } catch (error) {
      console.error('重置密码时出错:', error);
      alert('重置密码时出错，请稍后再试。');
    }
  } else {
    alert('两次密码输入不一致，请重新输入');
  }
}}

};
</script>

<style scoped>
.reset-password-page {
  height: 100vh; /* 视口高度 */
  background: url('../../img/background.png') no-repeat center center fixed; /* 背景图片 */
  background-size: cover; /* 背景图片覆盖 */
  display: flex; /* 使用 flexbox 居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.reset-password-container {
  text-align: center;
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px; /* 圆角 */
  padding: 40px; /* 内边距 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 阴影 */
  width: 400px; /* 宽度 */
}

input[type="password"] {
  width: 80%; /* 输入框宽度 */
  padding: 12px; /* 内边距 */
  margin: 8px 0; /* 上下外边距 */
}

button {
  width: 80%; /* 按钮宽度 */
  padding: 12px; /* 内边距 */
  margin-top: 10px; /* 增加按钮与输入框之间的距离 */
  margin-bottom: 10px;
  background-color: #5c6bc0; /* 按钮颜色 */
  color: white; /* 按钮文本颜色 */
  border: none; /* 去掉边框 */
  border-radius: 5px; /* 圆角 */
  cursor: pointer; /* 鼠标样式 */
}

button:hover {
  background-color: #3f51b5; /* 按钮悬停效果 */
}

.link {
  margin-top: 10px;
  color: #5c6bc0;
  cursor: pointer;
  text-decoration: underline;
}

.link:hover {
  color: #3f51b5;
}

.link-btn {
  display: block;
  width: 80%;
  padding: 12px;
  margin-top: 10px;
  background-color: #5c6bc0;
  color: white;
  text-align: center;
  border-radius: 5px;
  text-decoration: none;
}

.link-btn:hover {
  background-color: #3f51b5;
}
</style>
