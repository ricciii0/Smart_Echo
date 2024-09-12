<template>
  <div class="sidebar">
    <h2>智慧教学系统</h2>
    <ul>
      <li v-for="item in sidebarLinks" :key="item.name">
        <router-link :to="item.link" exact-active-class="active-link">{{ item.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Sidebar',
  computed: {
    ...mapState(['userIdType']),  // 从 Vuex 的状态中获取用户角色类型

    sidebarLinks() {
      if (this.userIdType === 'student') {
        return [
          { name: '首页', link: '/main' },
          { name: '资料管理', link: '/stu-resource-management' },
          { name: '在线练习', link: '/stu-online-exercise' },
          { name: '智能答疑', link: '/smart-machine' },
          { name: '社区交流', link: '/social-interaction' },
        ];
      } else if (this.userIdType === 'teacher') {
        return [
          { name: '首页', link: '/main' },
          { name: '教学内容', link: '/teaching-content' },
          { name: '资料管理', link: '/resource-management' },
          { name: '在线练习', link: '/online-exercise' },
          { name: '社区交流', link: '/tea-social-interaction' },
        ];
      }
      return [];
    },
  },
};
</script>


<style>
.sidebar {
  width: 200px;
  min-width: 200px;
  background: rgba(236, 240, 241, 0.5);
  padding: 20px;
  color: #34495e;
  display: flex;
  flex-direction: column;
  border-radius: 5px;
  text-align: center;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  z-index: 1;
  overflow: auto;
}

.sidebar h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 15px 0;
}

.sidebar a {
  color: #34495e;
  text-decoration: none;
  display: block;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
}

.sidebar a:hover {
  background-color: #999999;
  transform: scale(1.05);
}
</style>