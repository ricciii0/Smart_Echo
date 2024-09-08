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
        <div class="question-container">
    <div class="question-list">
      <h3>答疑转接</h3>
      <div
        v-for="(question, index) in questions"
        :key="question.id"
        :class="['question-item', { selected: selectedQuestionIndex === index }]"
        @click="selectQuestion(index)"
      >
        {{ question.id }}
      </div>
      <div class="pagination">
        <!-- Pagination controls can be added here -->
         
      </div>
    </div>
    
    <div class="question-detail">
      <h3>问题内容</h3>
      <p v-if="selectedQuestion">{{ selectedQuestion.content }}</p>
      <p v-else>请在左侧选择一个问题</p>
    </div>
    
    <div class="teacher-response">
      <textarea v-model="replyContent" placeholder="输入您的回复..."></textarea>
      <input type="file" @change="handleFileUpload"/>
      <button @click="submitReply">提交</button>
    </div>
  </div>
        <!-- 帖子区 -->
        <div class="post-area">
          <h3>讨论区</h3>
          <!-- 收藏夹按钮 -->
          <button @click="toggleFavorites">收藏夹</button>
          <!-- 发表帖子按钮，点击弹出发表帖子表单 -->
          <button @click="togglePostModal">发表帖子</button>
          
          <!-- 帖子列表，v-for循环渲染所有帖子 -->
          <div class="post" v-for="post in posts" :key="post.id">
            <div class="post-header">
              <span>{{ post.author }}</span>
              <span>{{ post.timestamp }}</span>
              <!-- 收藏按钮，添加/取消收藏 -->
              <button @click="toggleFavorite(post.id)">{{post.isFavorited?'取消收藏':'收藏'}}</button>
            </div>
            <!-- 帖子内容 -->
            <div class="post-content">{{ post.content }}</div>
            <div class="post-footer">
              <!-- 点赞按钮，点赞计数器增加 -->
              <button @click="likePost(post.id)">{{ post.likes }} 👍</button>
              <!-- 显示/隐藏评论按钮 -->
              <button @click="post.showComments = !post.showComments">
                {{ post.showComments ? '收起评论' : '查看评论' }}
              </button>
              <!-- 添加评论按钮 -->
              <button @click="commentPost(post.id)">+ 评论</button>
            </div>
            <!-- 评论区，显示所有评论 -->
            <div v-if="post.showComments" class="comment-section">
              <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
                {{ comment.content }}
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
              <div v-for="post in favoritePosts" :key="post.id" class="favorite-post">
                <div class="post-header">{{ post.author }} - {{ post.timestamp }}</div>
                <div class="post-content">{{ post.content }}</div>
              </div>
            </div>
            <!-- 没有收藏时显示的提示信息 -->
            <p v-else>404 not found</p>
          </div>
        </div>

        <!-- 发表帖子弹窗 -->
        <div v-if="showPostModal" class="modal-overlay" @click="togglePostModal">
          <div class="modal-content" @click.stop>
            <h3>发表帖子</h3>
            <button class="close-button" @click="togglePostModal">关闭</button>
            <!-- 发帖表单 -->
            <form @submit.prevent="submitPost">
              <div class="form-group">
                <label for="post-content">内容:</label>
                <textarea v-model="newPostContent" id="post-content" rows="5" placeholder="请输入帖子内容"></textarea>
              </div>
              <div class="form-group">
                <label for="file-upload">上传文件:</label>
                <input type="file" id="file-upload" @change="handleFileUpload" />
              </div>
              <!-- 提交按钮 -->
              <button type="submit">提交</button>
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

export default {
  name: 'SocialInteraction',
  components: {
    Sidebar,
    UserControls,
  },
  data() {
    return {
      username: 'admin', // 当前用户名
      selectedClass: '班级1', // 选中的班级
      posts: [ // 帖子数据
        { id: 1, author: '学生1', timestamp: '1小时前', content: '这是一个帖子内容', likes: 0, showComments: false, comments: [ { id: 1, content: '这是第一条评论' },
            { id: 2, content: '这是第二条评论' }],isFavorited:false },
        // 其他帖子...
      ],
      questions: [
        { id: '1', content: '这是第一个问题的内容。' },
        { id: '2', content: '这是第二个问题的内容。' },
        { id: '3', content: '这是第三个问题的内容。' }
      ],
      favoritePosts: [], // 收藏的帖子
      showFavorites: false, // 是否显示收藏夹弹窗
      showPostModal: false, // 是否显示发表帖子弹窗
      newPostContent: '', // 新帖子的内容
      uploadedFile: null, // 上传的文件
      selectedQuestionIndex: null,
      replyContent: '',
      selectedFile: null
    };
  },
  computed: {
    selectedQuestion() {
      return this.selectedQuestionIndex !== null
        ? this.questions[this.selectedQuestionIndex]
        : null;
    }
  },



  methods: {
    selectQuestion(index) {
      this.selectedQuestionIndex = index;
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    submitReply() {
      if (this.selectedQuestionIndex === null || !this.replyContent) {
        alert('请填写回复内容');
        return;
      }

      // 处理提交逻辑，例如通过 API 发送数据
      console.log('提交问题:', this.questions[this.selectedQuestionIndex].id);
      console.log('回复内容:', this.replyContent);
      console.log('上传的文件:', this.selectedFile);

      // 清理表单
      this.replyContent = '';
      this.selectedFile = null;
    },
    // 切换收藏夹显示/隐藏
    toggleFavorites() {
      this.showFavorites = !this.showFavorites;
    },
    // 收藏或取消收藏帖子
    toggleFavorite(postId) {
      const post = this.posts.find(p => p.id === postId);
      if (post && !this.favoritePosts.includes(post)) {
        this.favoritePosts.push(post);
      }
	  post.isFavorited=!post.isFavorited;
    },
    // 切换发表帖子弹窗显示/隐藏
    togglePostModal() {
      this.showPostModal = !this.showPostModal;
    },
    // 点赞帖子
    likePost(postId) {
      const post = this.posts.find(p => p.id === postId);
      if (post) {
        post.likes++;
        alert(`点赞帖子 ID: ${postId}`);
      }
    },
    // 处理文件上传
    handleFileUpload(event) {
      this.uploadedFile = event.target.files[0];
    },
    // 添加评论
    commentPost(postId) {
      const comment = prompt('请输入您的评论:');
      const post = this.posts.find(p => p.id === postId);
      if (comment && post) {
        post.comments.push({ id: post.comments.length + 1, content: comment });
      }
    },
    // 提交帖子
    submitPost() {
      if (this.newPostContent || this.uploadedFile) {
        const newPost = {
          id: this.posts.length + 1,
          author: this.username,
          timestamp: '刚刚',
          content: this.newPostContent || `文件上传: ${this.uploadedFile.name}`,
          likes: 0,
          showComments: false,
          comments: [],
        };
        this.posts.push(newPost);
        this.newPostContent = '';
        this.uploadedFile = null;
        this.togglePostModal(); // 关闭发表帖子弹窗
      } else {
        alert('请填写内容或上传文件。');
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
  background-image: url('../../img/background.png');
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
  width: 300px;
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

	 max-height: 100px; /* 固定最大高度 */
	  overflow-y: auto; /* 启用垂直滚动 */
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.post-footer {
  display: flex;
  justify-content: space-between;
}
.post-area {
  background: rgba(255, 255, 255, 0.8);
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
  box-shadow: 5px;
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

</style>
