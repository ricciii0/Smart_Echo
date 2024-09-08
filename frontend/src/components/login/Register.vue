<template>
  <div class="register-page">
	  <Sidebar />
	    <router-view />
	  
    <div class="register-container">
      <h1>注册</h1>
      <form @submit.prevent="handleRegister">
        <select v-model="role" @change="toggleFields">
          <option value="" disabled selected>选择身份</option>
          <option value="student">学生</option>
          <option value="teacher">教师</option>
        </select>

        <div v-if="role === 'student'">
          <input type="text" v-model="studentId" placeholder="学号" required />
          <input type="text" v-model="studentName" placeholder="姓名" required />
          <input type="text" v-model="studentClass" placeholder="班级" required />
		  
		  <input type="password" v-model="password" placeholder="密码" required />
		  <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
          <div v-if="classError" class="error">{{ classError }}</div>
        </div>

        <div v-if="role === 'teacher'">
          <input type="text" v-model="teacherId" placeholder="教师号" required />
          <input type="text" v-model="teacherName" placeholder="姓名" required />
          <input type="text" v-model="teacherSubject" placeholder="科目" required />
          <input type="text" v-model="teacherEmail" place holder="邮箱号" required />


		  <input type="password" v-model="password" placeholder="密码" required />
		  <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
        </div>


        <button type="submit" class="btn">注册</button>

      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: '',
      studentId: '',
      studentName: '',
      studentClass: '',
      teacherId: '',
      teacherName: '',
      password: '',
      confirmPassword: '',
      classError: '',
    };
  },
  methods: {
    toggleFields() {
      this.classError = ''; // 重置错误信息
    },
    handleRegister() {
      // 注册逻辑
      if (this.password !== this.confirmPassword) {
        alert('密码不匹配');
        return;
      }

      // 其他注册逻辑...
      alert('注册成功！');
	  
	        // 自动返回登录页面
	        this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.register-page {
  height: 100vh; /* 视口高度 */
  background: url('../../img/background.png') no-repeat center center fixed; /* 背景图片 */
  background-size: cover; /* 背景图片覆盖 */
  display: flex; /* 使用 flexbox 居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.register-container {
  text-align: center;
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px; /* 圆角 */
  padding: 40px; /* 内边距 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 阴影 */
  width: 400px; /* 宽度 */
}

input[type="text"],
input[type="password"],
select {
  width: 80%; /* 输入框和选择框宽度 */
  padding: 12px; /* 内边距 */
  margin: 10px 0; /* 上下外边距 */
}

button {
  width: 80%; /* 按钮宽度 */
  padding: 12px; /* 内边距 */
  margin-top: 20px; /* 增加按钮与输入框之间的距离 */
  background-color: #5c6bc0; /* 按钮颜色 */
  color: white; /* 按钮文本颜色 */
  border: none; /* 去掉边框 */
  border-radius: 5px; /* 圆角 */
  cursor: pointer; /* 鼠标样式 */
}

.error {
  color: red; /* 错误信息颜色 */
  margin-top: 10px; /* 上边距 */
}
</style>