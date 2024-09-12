// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './js/router.js'; // 引入路由实例
import store from './store/index.js'; // 引入 Vuex store

const app = createApp(App);

// 使用 router 和 store
app.use(router);
app.use(store);  // 添加 Vuex store

app.mount('#app');
