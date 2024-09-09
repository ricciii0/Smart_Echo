import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/login/Login.vue'; // 引入 Login 组件
import ForgotPassword from '../components/login/ForgotPassword.vue'; // 引入 ForgotPassword 组件
import Register from '../components/login/Register.vue'; // 引入 Register 组件
import Main from '../components/main/Main.vue'; // 主页面
import ResourceManagement from'../components/zlgl/ResourceManagement.vue';
import stuResourceManagement from'../components/zlgl/stuResourceManagement.vue';
import TeachingContent from'../components/jxnr/TeachingContent.vue';
import SmartMachine from'../components/znjq/SmartMachine.vue';
import teaSmartMachine from'../components/znjq/teaSmartMachine.vue';
import SocialInteraction from'../components/sqjl/SocialInteraction.vue';
import teaSocialInteraction from'../components/sqjl/teaSocialInteraction.vue';
import OnlineExercise from'../components/zxlx/OnlineExercise.vue';
import stuOnlineExercise from'../components/zxlx/stuOnlineExercise.vue';
import ResetPassword from "../components/login/reset-password.vue";




const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
    {
      path: '/main',
      name: 'Main',
      component: Main,
    },
	{
	  path: '/resource-management',
	  name: 'ResourceManagement',
	  component: ResourceManagement,
	},
	{
		path: '/stu-resource-management',
		name: 'stuResourceManagement',
		component: stuResourceManagement,
	  },
	{
	  path: '/teaching-content',
	  name: 'TeachingContent',
	  component: TeachingContent,
	},
	{
	  path: '/smart-machine',
	  name: 'SmartMachine',
	  component: SmartMachine,
	
	},
	{
		path: '/tea-smart-machine',
		name: 'teaSmartMachine',
		component: teaSmartMachine,
	  
	  },
	{
	  path: '/social-interaction',
	  name: 'SocialInteraction',
	  component: SocialInteraction,
	},
	{
	  path: '/tea-social-interaction',
	  name: 'teaSocialInteraction',
	  component: teaSocialInteraction,
	},
	{
	  path: '/online-exercise',
	  name: 'OnlineExercise',
	  component: OnlineExercise,
	},
	{
		path: '/stu-online-exercise',
		name: 'stuOnlineExercise',
		component: stuOnlineExercise,
	  },
	{
		path: '/reset-password',
		name: 'ResetPassword',
		component: ResetPassword,
	  },

	
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;