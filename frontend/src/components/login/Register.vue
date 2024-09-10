<template>
  <div class="register-page">

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
          <input type="text" v-model="teacherEmail" placeholder="邮箱号" required />
<input type="text" v-model="teacherClass" placeholder="班级（若有多个请用逗号隔开）" required />

		  <input type="password" v-model="password" placeholder="密码" required />
		  <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
        </div>


        <button type="submit" class="btn">注册</button>

      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';


export default {

  data() {
    return {
      role: '',
      studentId: '',
      studentName: '',
      studentClass: '',
      teacherId: '',
      teacherName: '',
        teacherSubject: '',
      teacherEmail: '',
      teacherClass: '',
      password: '',
      confirmPassword: '',
      classError: '',
    };
  },
  methods: {
    toggleFields() {
      this.classError = ''; // 重置错误信息
    },
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('密码不匹配');
        return;
      }

      const payload = {
        role: this.role,
        password: this.password,
      };

      // 根据身份处理不同的注册信息
      if (this.role === 'student') {
        payload.studentId = this.studentId;
        payload.studentName = this.studentName;
        payload.studentClass = this.studentClass;
      } else if (this.role === 'teacher') {
        payload.teacherId = this.teacherId;
        payload.teacherName = this.teacherName;
        payload.teacherSubject = this.teacherSubject;
        payload.teacherEmail = this.teacherEmail;
      }

      try {
        // 发送注册请求到后端
        const response = await axios.post('http://127.0.0.1:5000/register', payload);

        if (response.data.success) {
          alert('注册成功！');
          this.$router.push('/'); // 注册成功后跳转到登录页面
        } else {
          alert(response.data.message || '注册失败');
        }
      } catch (error) {
        console.error('注册请求失败:', error);
        alert('注册请求失败，请稍后再试');
      }
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