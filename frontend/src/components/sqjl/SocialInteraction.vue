<template>
  <div class="main-container">
    <!-- 左侧边栏 -->
    <Sidebar />
    <!-- 动态路由视图，显示不同页面内容 -->
    <router-view />

    <div class="main-content">
      <!-- 用户控件，显示用户名及班级选择，支持注销 -->
      <UserControls :username="username" v-model="selectedClass" @logout="handleLogout" />

      <div class="content-area">
        <!-- 帖子区 -->
        <div class="post-area">
          <h3>讨论区</h3>
          <br>
          <!-- 收藏夹按钮 -->
          <button @click="toggleFavorites">收藏夹</button>
          <!-- 发表帖子按钮，点击弹出发表帖子表单 -->
          <button @click="togglePostModal">发表帖子</button>

          <!-- 帖子列表，v-for循环渲染所有帖子 -->
          <div class="post" v-for="post in posts" :key="post.post_id">
            <div class="post-header">
              <span>{{ post.poster_id }}</span>
              <span>{{ post.post_time }}</span>
              <!-- 收藏按钮，添加/取消收藏 -->
              <button @click="toggleFavorite(post.post_id, post.is_favorite)">{{post.is_favorite?'取消收藏':'收藏'}}</button>
            </div>
            <!-- 帖子内容 -->
             <div class="post-title">{{ post.title }}</div>
            <div class="post-content">{{ post.content }}</div>
            <div class="post-footer">
              <!-- 点赞按钮，点赞计数器增加 -->
              <button @click="likePost(post.post_id)">{{ post.likes_num }} 👍</button>
              <!-- 显示/隐藏评论按钮 -->
              <button @click="post.showComments = !post.showComments">
                {{ post.showComments ? '收起评论' : '查看评论' }}
              </button>
              <!-- 添加评论按钮 -->
              <button @click="commentPost(post.post_id)">+ 评论</button>
            </div>
            <!-- 评论区，显示所有评论 -->
            <div v-if="post.showComments" class="comment-section">
              <div v-for="comment in post.comments" :key="comment.reply_id" class="comment-item">
                 <div class="comment-content">{{ comment.content }}</div>
                <div class="comment-footer">{{comment.publisher_id}}    {{comment.reply_time}}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 收藏夹弹窗，显示收藏的帖子 -->
        <div v-if="showFavorites" class="modal-overlay" @click="toggleFavorites">
          <div class="modal-content" @click.stop>
            <h3>收藏夹</h3>
            <button class="close-button" @click="toggleFavorites">关闭</button>
            <!-- 收藏列表，v-for渲染收藏帖子 -->
            <div v-if="favoritePosts.length > 0" class="favorites-list">
              <div v-for="favorite in favoritePosts" :key="favorite.favorite_id" class="favorite-post">
                <div class="post-header">{{ favorite.favorite_id }} - {{favorite.favorite_time }}</div>
                <div class="post-content">{{ favorite.title }}</div>
              </div>
            </div>
            <!-- 没有收藏时显示的提示信息 -->
            <p v-else>收藏夹为空</p>
          </div>
        </div>

        <!-- 发表帖子弹窗 -->
        <div v-if="showPostModal" class="modal-overlay" @click="togglePostModal">
          <div class="modal-content" @click.stop>
            <h3>发表帖子</h3>
            <button class="close-button" @click="togglePostModal">关闭</button>
            <!-- 发帖表单 -->
             <br>
            <form @submit.prevent="submitPost">
              <div class="form-group">
                <label for="post-title">标题:</label>
                <textarea v-model="newPostTitle" class="post-add" rows="1" placeholder="请输入帖子标题"></textarea>
                <label for="post-content">内容:</label>
                <textarea v-model="newPostContent" class="post-content" rows="5" placeholder="请输入帖子内容"></textarea>
              </div>
              <!--<div class="form-group">
                <label for="file-upload">上传文件: </label>
                <input type="file" id="file-upload" @change="handleFileUpload" />
              </div> -->

              <!-- 提交按钮 -->
               <br>
              <button type="submit" id="favorite-submit">提交</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../shared/Sidebar.vue';
import UserControls from '../shared/UserControls.vue';
import axios from 'axios';

export default {
  name: 'OnlineExercise',
  components: {
    Sidebar,
    UserControls,
  },
  data() {
    return {
      username: 'admin', // 当前用户名
      userid: ' ', //用户id
      selectedClass: '班级1', // 选中的班级

      posts: [],
      favoritePosts: [], // 收藏的帖子

      showFavorites: false, // 是否显示收藏夹弹窗
      showPostModal: false, // 是否显示发表帖子弹窗

      newPostContent: '', // 新帖子的内容
      //uploadedFile: null, // 上传的文件
      newPostTitle: '',
    };
  },
  created(){
    this.loadPosts();

    this.loadFavorite();
  },
  methods: {
    //加载帖子
    async loadPosts() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/student/community/get_posts');
      this.posts = response.data;

      for (const post of this.posts) {
        this.isFavorited(post.post_id);
        this.loadComments(post.post_id);
      }
      } catch (error) {
        console.log(error);
      }
    },
    isFavorited(postId){
      axios.get('http://127.0.0.1:5000/student/community/is_favorite', {
        params: { 'post_id': postId, 'user_id': this.userid}
    })
      .then(response =>{
        const post = this.posts.find(p => p.post_id === postId);
        post.is_favorite = response.data.is_favorite;
      })
      .catch(error =>{
        console.log(error);
      })
    },
    loadFavorite(){
      axios.get('http://127.0.0.1:5000/student/community/get_favorite',{
        params: {'user_id': this.userid}
      })
      .then(response =>{
        this.favoritePosts = response.data;
      })
      .catch(error =>{
        console.log(error);
      })
    },
    loadComments(postId){
      axios.get('http://127.0.0.1:5000/student/community/get_replies', {
        params: {'post_id': postId}
      })
      .then(response =>{
        const post = this.posts.find(p => p.post_id === postId);
        post.comments = response.data;
        post.showComments = false;
      })
      .catch(error =>{
        console.log(error);
      })
    },
    // 切换收藏夹显示/隐藏
    toggleFavorites() {
      this.showFavorites = !this.showFavorites;
    },
    // 收藏或取消收藏帖子
    toggleFavorite(postId) {
      const post = this.posts.find(p =>p.post_id === postId);
      if(post.is_favorite){
        //  删除
        axios.delete('http://127.0.0.1:5000/student/community/delete_favorite', {
          data: {'user_id': this.userid, 'post_id': postId},
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response =>{
            console.log(response);
        })
        .catch(error =>{
          console.log(error);
        })
        const favorite = this.favoritePosts.find(f => f.post_id === postId);
        post.favorites_num--;
        this.favoritePosts.pop(favorite);
      }
      else{
        axios.post('http://127.0.0.1:5000/student/community/add_favorite', {
          'user_id': this.userid,
          'title': post.title,
          'post_id': postId,
        })
        .then(response =>{
          this.favoritePosts.push(response.data);
        })
        .catch(error =>{
          console.log(error);
        })
        post.favorites_num++;
      }
      post.is_favorite = !post.is_favorite;
    },

    // 切换发表帖子弹窗显示/隐藏
    togglePostModal() {
      this.showPostModal = !this.showPostModal;
    },

    // 点赞帖子
    likePost(postId) {
      const post = this.posts.find(p => p.post_id === postId);
      if (post) {
        post.likes_num++;
        axios.post('http://127.0.0.1:5000/student/community/add_likes_num', {'post_id': postId})
        .then(response=>{
          console.log(response);
        })
        .catch(error =>{
          console.log('error:', error);
        })
      }
    },

    // 处理文件上传
    handleFileUpload(event) {
      this.uploadedFile = event.target.files[0];
    },
    // 添加评论
    commentPost(postId) {
      const comment = prompt('请输入您的评论:');
      if(comment){
        axios.post('http://127.0.0.1:5000/student/community/create_replies', {
        'content': comment,
        'publisher_id': this.userid,
        "post_id": postId,
      })
        .then(response=>{
          const post = this.posts.find(p => p.post_id === postId);
          post.comments.push(response.data);
          post.replies_num ++;
        })
        .catch(error =>{
          console.log('error:', error);
        })
      }

    },
    // 提交帖子
    submitPost() {
      if (this.newPostContent && this.newPostTitle) {
        const newPost = {
          poster_id: this.userid,
          content: this.newPostContent,
          title: this.newPostTitle,
        };
        axios.post('http://127.0.0.1:5000/student/community/create_posts', newPost, {
          headers:{
            'Content-Type': 'application/json'
          }
        })
        .then(response =>{
          response.data.is_favorite = false;
          response.data.is_like = false;
          response.data.comments = [];
          this.posts.push(response.data);
        })
        .catch(error =>{
          console.log(error)
        })

        this.newPostContent = '';
        this.newPostTitle = '';
        //this.uploadedFile = null;
        this.togglePostModal(); // 关闭发表帖子弹窗
      } else {
        alert('标题与内容不能为空！');
      }
    },
  },
};
</script>

<style scoped>
/* 页面布局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  margin: 0;
  font-family: 'Arial', sans-serif;
}

.main-container {
  display: flex;
  background-image: url('../../../public/img/background.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
  margin:0;
}

.main-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  margin-left: 20px;
  overflow: auto;
}

/* 下拉区样式 */
select,
input[type="text"],
input[type="file"] {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ced4da;
  background-color: #fff;
  color: #495057;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

select:hover {
  border-color: #80bdff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* 帖子区样式 */
.post-area-wrapper {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 允许内容从上到下 */
  height: 100vh; /* 占满整个视口高度 */
  overflow: auto; /* 开启滚动 */
}

.post-area {
	width: 100%; /* 占满父容器宽度 */
	 height:400px;
	 overflow-y: auto;
	 padding:20px;


  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 30px;
  border-radius: 5px;
}

.post {
  max-height:200px;
  overflow-y: auto;
  padding: 10px;
  margin-top: 30px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
}

.post-header,
.post-footer {
  display: flex;
  justify-content: space-between;
}

.comment-section {
  margin-top: 10px;
}

.comment-item {
  padding: 5px;
  background-color: #f1f1f1;
  margin-top: 5px;
}

/* 按钮样式 */
button {
  padding: 8px 10px;
  border-radius: 5px;
  border: none;
  background: rgb(255, 255, 255);
  color: black;
  font-weight: bold;
  font-size: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 10px;
}

button:hover {
  background-color: #f1f1f1;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 600px;
  height: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #CD5C5C;
  color: white;
  padding: 5px;
  border: none;
  cursor: pointer;
}

.close-button:hover {
  background: darkred;
}


.question-area {
  display: flex;
  gap: 20px; /* 左右间距 */
}

.post {

  max-height: 200px; /* 固定最大高度 */
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 8px;
}

.post-title {
    font-size: 12px; /* 字体大小 */
    font-weight: bold; /* 字体加粗 */
    color: #333; /* 字体颜色 */
    margin-bottom: 6px; /* 与内容的间距 */
    text-align: center;
}

/* 帖子内容样式 */
.post-content {
    font-size: 10px; /* 字体大小 */
  font-weight: bold;
    line-height: 1.6; /* 行高 */
    color: #666; /* 字体颜色 */
    margin-bottom: 20px; /* 与底部的间距 */
}

.post-footer {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
}
.post-area {
  background: rgba(255, 255, 255, 0.8);
  height: 600px;
  padding: 30px;
  margin-top: 30px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}


.question-container {
  display: flex;
  flex: 1;

}

.question-list {
  width: 100px; /* 左侧提问列表宽度 */
   max-height: 400px; /* 固定最大高度 */
    overflow-y: auto; /* 启用垂直滚动 */
  background: rgba(255, 255, 255, 0.8);
  border-radius: 5px;
  padding: 10px;

  margin-right: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.question-item {
  padding: 10px;
  margin-bottom: 5px;
  margin-right: 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
  cursor: pointer;
  text-align: center;
}

.question-item:hover {
  background-color: #e7e7e7;
}

.selected {
  background-color: #b5d3f5 !important;
}
input[type="file"] {
  margin-top: 10px;
  margin-right: 10px;
}
.pagination {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.question-detail {
  flex: 1; /* 右侧提问内容区域 */
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 5px;

}


.controls {
  display: flex;
  justify-content: space-between;
}

.controls input[type="file"] {
  border: 1px solid #ced4da;
  padding: 5px;
  border-radius: 5px;
}


.teacher-response {
  margin-top: 15px;
  margin-left:30px;
  margin-right: 20px;

}

textarea {
  width: 100%;
  padding: 10px;
  height: 200px;
  border-radius: 5px;
  border: 1px solid #ced4da;
  background-color: #fff;
  color: #495057;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-bottom: 10px;
}

.favorite-post {
  border: 1px solid #ddd;
  padding: 10px;
  margin-top:20px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.comment-content{
  font-size: 10px;
}
.comment-footer{
  display: flex;
  justify-content: right;
  font-size: 5px;
}

.favorite-submit{
  display: flex;
  justify-content: center;
}


</style>
