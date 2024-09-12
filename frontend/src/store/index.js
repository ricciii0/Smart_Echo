// src/store/index.js
import { createStore } from 'vuex';

// 创建 store 实例
const store = createStore({
  state: {
    userIdType: '',  // 用于存储用户角色类型，例如 'student' 或 'teacher'
  },
  mutations: {
    setUserIdType(state, userIdType) {
      state.userIdType = userIdType;  // 更新用户类型
    },
  },
  actions: {
    login({ commit }, { user_type }) {
      commit('setUserIdType', user_type);  // 将角色类型存储到 Vuex
    },
  },
  getters: {
    getUserIdType: (state) => state.userIdType,  // 提供一个 getter 来访问用户类型
  },
});

// 默认导出 store 实例
export default store;
