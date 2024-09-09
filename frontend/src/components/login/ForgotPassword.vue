<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <h1>忘记密码</h1>
      <p>请输入您的邮箱以重置密码：</p>
      <input type="email" v-model="email" placeholder="请输入邮箱" required />
       <!-- 验证码输入框 -->
      <div class="verification-container">
        <input type="text" v-model="verificationCode" placeholder="请输入验证码" required />
        <button class="send-code-btn" @click="sendVerificationCode">发送验证码</button>
      </div>
        <router-link
        v-if="verificationCode === correctCode"
        to="/reset-password"
        class="router-link-btn"
      >
        确定
      </router-link>
      <div class="link" @click="$router.push('/')">返回登录</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
       verificationCode: '',
      correctCode: '123456', // 假设这是正确的验证码，实际情况应该从服务器获取并验证

    };
  },
  methods: {
     sendVerificationCode() {
      alert(`验证码已发送到 ${this.email}`);
    },



  },
};
</script>

<style scoped>
.forgot-password-page {
  height: 100vh; /* 视口高度 */
  background: url('../../img/background.png') no-repeat center center fixed; /* 背景图片 */
  background-size: cover; /* 背景图片覆盖 */
  display: flex; /* 使用 flexbox 居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.forgot-password-container {
  text-align: center;
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px; /* 圆角 */
  padding: 40px; /* 内边距 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 阴影 */
  width: 400px; /* 宽度 */
}

input[type="email"] {
  width: 80%; /* 输入框宽度 */
  padding: 12px; /* 内边距 */
  margin: 8px 0; /* 上下外边距 */
}
input[type="text"] {
  width:50%;
  padding:12px;
  display:flex;

}

.verification-container {
  display: flex;

  align-items: center;
    justify-content: center; /* 居中 */

}

.send-code-btn {
  width:100px;
  padding: 12px;
  margin-left: 10px;
  background-color: #5c6bc0; /* 按钮颜色 */
  color: white; /* 按钮文本颜色 */
  border: none; /* 去掉边框 */
  border-radius: 5px; /* 圆角 */
  cursor: pointer; /* 鼠标样式 */
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
</style>