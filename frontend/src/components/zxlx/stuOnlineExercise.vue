<template>
	<div class="main-container">
		<Sidebar />
		<router-view />

		<div class="main-content">
			<UserControls :username="username" v-model="selectedClass" @logout="handleLogout" />

			<div class="content-area">
				<div class="student-submissions">
					<h3>待做练习</h3>
					<table class="submission-table">
						<thead>
							<tr>
								<th>序号</th>
								<th>发布老师</th>
								<th>练习名称</th>
								<th>发布时间</th>
								<th>操作</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(exercise, index) in Exercises" :key="index">
								<td>{{ index + 1 }}</td>
								<td>{{ exercise.teacher }}</td>
								<td>{{ exercise.title }}</td>
								<td>{{ exercise.uploadTime }}</td>
								<td>
									<button @click="download(exercise)">下载练习</button>
									<button @click="triggerFileInput(exercise)">上传答案</button>
									<input ref="fileInput" type="file" style="display: none"
										@change="handleFileChange" />
								</td>
							</tr>
						</tbody>
					</table>
					<div v-if="selectedRecord">
						<h4>学生答案</h4>
						<p>{{ selectedRecord.studentAnswer }}</p>
						<input v-model="score" placeholder="输入得分" type="number" />
						<textarea v-model="feedback" placeholder="输入反馈"></textarea>
						<button @click="submitFeedback">提交反馈</button>
					</div>
				</div>

				<div class="student-submissions">
					<h3>已完成练习</h3>
					<table class="submission-table">
						<thead>
							<tr>
								<th>序号</th>
								<th>发布老师</th>
								<th>练习标题</th>
								<th>提交时间</th>
								<th>批改时间</th>
								<th>得分</th>
								<th>老师反馈</th>
								<th>操作</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(record, index) in historyRecords" :key="index">
								<td>{{ index + 1 }}</td>
								<td>{{ record.teacher }}</td>
								<td>{{ record.title }}</td>
								<td>{{ record.submitTime }}</td>
								<td>{{ record.checkTime }}</td>
								<td>{{ record.score }}</td>
								<td>{{ record.feedback }}</td>
								<td>
									<button @click="viewSubmission(record)">查看详情</button>
								</td>
							</tr>
						</tbody>
					</table>
					<div v-if="selectedRecord">
						<h4>学生答案</h4>
						<p>{{ selectedRecord.studentAnswer }}</p>
						<input v-model="score" placeholder="输入得分" type="number" />
						<textarea v-model="feedback" placeholder="输入反馈"></textarea>
						<button @click="submitFeedback">提交反馈</button>
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
		mounted() {
			this.getExercise();
			this.getRecord();
		},

		data() {
			return {
				Exercises: [
					// 添加更多示例资源以便于分页
					{
						teacher: '加载中...',
						title: '加载中...',
						uploadTime: '加载中...',
					},
				],
				historyRecords: [
					// 添加更多示例资源以便于分页
					{
						teacher: '加载中...',
						title: '加载中...',
						submitTime: '加载中...',
						checkTime: '加载中...',
						score: '加载中...',
						feedback: '加载中...',
					},
				],
				username: 'admin',
				selectedClass: '班级1',
				selectedKnowledgeQuestion: null,
				selectedSubmission: null,
				knowledgeBase: [], // 假设知识库数据
				selectedRecord: null, // 当前查看的提交记录
				score: '',
				feedback: '',
			};
		},
		methods: {
			logout() {
				alert('已退出登录');
				this.$router.push('/');
			},
			uploadExercise() {
				const fileInput = this.$refs.uploadFile;
				if (!fileInput.files.length) {
					alert('请先选择文件进行上传');
					return;
				}

				const file = fileInput.files[0];
				const reader = new FileReader();
				reader.onload = (e) => {
					const content = e.target.result;
					this.parseExerciseContent(content);
				};
				reader.readAsText(file);
			},
			parseExerciseContent(content) {
				const lines = content.split('\n');
				lines.forEach((line) => {
					if (line.trim()) {
						this.exercises.push({
							id: this.exercises.length + 1,
							title: `练习题 ${this.exercises.length + 1}`,
							content: line,
							score: 0,
							feedback: '',
						});
					}
				});
				alert('练习题上传成功');
			},
			triggerFileInput(exercise) {
				this.$refs.fileInput.click();
				this.currentExerciseId = exercise['id'];
			},
			async handleFileChange(event) {
				// alert(this.currentExerciseId)
				const file = event.target.files[0];
				if (file) {
					const formData = new FormData();
					formData.append('file', file);
					formData.append('exerciseId', this.currentExerciseId); // 替换成实际 ID
					try {
						const response = await axios.post('http://127.0.0.1:5000/oe/raiseAnswer/', formData, {
							headers: {
								'Content-Type': 'multipart/form-data'
							}
						});
						alert('文件上传成功:', response.data);
					} catch (error) {
						alert('文件上传失败:', error);
					}
					this.getExercise();
					this.getRecord();
				}
			},
			getExercise() {
				let stuid = 2;
				axios.post('http://127.0.0.1:5000/oe/print/', {
						id: stuid
					})
					.then(result => {
						this.Exercises = result.data;
					});
			},
			getRecord() {
				let stuid = 2;
				axios.post('http://127.0.0.1:5000/oe/record/', {
						id: stuid
					})
					.then(result => {
						this.historyRecords = result.data;
					});
			},
			download(exercise) {
				axios({
						url: `http://127.0.0.1:5000/oe/download/`,
						method: 'POST',
						data: {
							exercise
						}, //使用POST方式将 id 作为请求体的一部分
						responseType: 'blob' // 指定响应类型为 Blob
					})
					.then(response => {
						const url = window.URL.createObjectURL(new Blob([response.data]));
						const a = document.createElement('a');
						a.href = url;
						a.download = exercise.exercisename;
						document.body.appendChild(a);
						a.click();
						document.body.removeChild(a);
					})
					.catch(error => {
						console.error('Error:', error);
					});
			},
			addToExercises() {
				const question = this.knowledgeBase.find(q => q.id === this.selectedKnowledgeQuestion);
				if (question) {
					this.exercises.push({
						id: this.exercises.length + 1,
						title: question.title,
						content: question.content,
						score: 0,
						feedback: '',
					});
					alert('题目已添加到练习');
				}
			},
			viewSubmission(record) {
				// 打开新窗口预览文件
				window.open(`http://127.0.0.1:5000/oe/preview_material_stu/${record.id}`, '_blank');
			},
			submitFeedback() {
				if (this.selectedRecord) {
					this.selectedRecord.score = this.score;
					this.selectedRecord.feedback = this.feedback;
					alert('反馈已提交');
					this.score = '';
					this.feedback = '';
				}
			},
		},
	};
</script>

<style scoped>
	/* =========================
     通用样式
  ========================= */
	* {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	html,
	body {
		height: 100%;
		margin: 0;
		font-family: 'Arial', sans-serif;
	}

	/* =========================
     主容器样式
  ========================= */
	.main-container {
		display: flex;
		background-image: url('../../../public/img/background.png');
		background-size: cover;
		/* 使图片覆盖整个容器 */
		background-position: center;
		/* 图片居中 */
		background-repeat: no-repeat;
		/* 不重复背景图片 */
		height: 100vh;
		/* 填满整个视口高度 */
		margin: 0;
	}



	/* =========================
     提交记录表格样式
  ========================= */
	.submission-table {
		width: 100%;
		border-collapse: collapse;
		margin-bottom: 20px;
	}

	.submission-table th,
	.submission-table td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: center;
	}

	.submission-table th {
		background-color: #f2f2f2;
	}

	.submission-table tr:hover {
		background-color: #f1f1f1;
	}

	/* =========================
     主内容样式
  ========================= */
	.main-content {
		flex: 1;
		padding: 20px;
		display: flex;
		flex-direction: column;
		margin-left: 20px;
		overflow: auto;
	}

	.header {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		margin-bottom: 20px;
	}

	.user-controls {
		display: flex;
		align-items: center;
	}

	.user-controls span {
		margin-right: 20px;
	}

	.welcome-message {
		margin-left: 10px;
		margin-right: 20px;
		font-size: 0.9em;
		color: #34495e;
	}

	/* =========================
     内容区域样式
  ========================= */
	.content-area {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	/* =========================
     发布练习样式
  ========================= */
	.exercise-publish,
	.student-submit,
	.teacher-feedback,
	.history-records {
		margin-bottom: 20px;
	}

	h3 {
		margin-bottom: 10px;
		font-size: 1.5em;
		/* 增大字体 */
		color: #34495e;
		/* 更深的颜色 */
		margin-bottom: 10px;
		/* 增加底部间距 */
		margin-top: 10px;
		padding-bottom: 5px;
		/* 增加内边距 */
		text-align: left;
		/* 对齐方式可以根据需要调整 */
	}

	h4 {
		font-size: 1.25em;
		/* 调整字体大小 */
		color: #007bff;
		/* 明亮的颜色 */
		margin-bottom: 10px;
		/* 增加底部间距 */
		font-weight: bold;
		/* 加粗字体 */
	}

	/* =========================
     历史记录样式
  ========================= */
	.history-table {
		width: 100%;
		border-collapse: collapse;
	}

	.history-table th,
	.history-table td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: center;
	}

	.history-table th {
		background-color: #f2f2f2;
	}

	.history-table tr:hover {
		background-color: #f1f1f1;
	}

	/* =========================
     输入框和按钮样式
  ========================= */


	/* =========================
     搜索栏样式
  ========================= */
	.search-bar {
		display: flex;
		align-items: center;
		margin-bottom: 20px;
		/* 添加底部边距 */
	}

	.search-bar input,
	.search-bar select {
		margin-right: 10px;
		/* 添加右边距 */
	}

	/* =========================
     表格样式
  ========================= */
	.resource-table {
		width: 100%;
		max-height: 400px;
		/* 最大高度 */
		border-collapse: collapse;
		/* 合并边框 */
		overflow-y: auto;
		/* 允许竖向滚动 */
		font-size: 14px;
		/* 表格字体大小 */
		margin-bottom: 20px;
		/* 表格底部间距 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		/* 盒子阴影 */
		border-radius: 5px;
		/* 圆角 */
	}

	.resource-table th,
	.resource-table td {
		border: 1px solid #ddd;
		/* 添加边框 */
		padding: 8px;
		/* 添加内边距 */
		text-align: center;
		/* 内容居中 */
	}

	.resource-table th {
		background-color: #f2f2f2;
		/* 表头背景颜色 */
	}

	.resource-table tr:hover {
		background-color: #f1f1f1;
		/* 鼠标悬停时行背景颜色 */
	}

	/* =========================
     上传练习部分样式
  ========================= */
	.exercise-upload {
		background-color: rgba(249, 249, 249, 0.5);
		/* 背景颜色 */
		border: 1px solid #ddd;
		/* 边框 */
		border-radius: 5px;
		/* 圆角 */
		padding: 15px;
		/* 内边距 */
		margin-bottom: 20px;
		/* 底部间距 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		/* 阴影效果 */
	}

	/* =========================
     知识库选择部分样式
  ========================= */
	.knowledge-base {
		background-color: rgba(249, 249, 249, 0.5);
		/* 背景颜色 */
		border: 1px solid #ddd;
		/* 边框 */
		border-radius: 5px;
		/* 圆角 */
		padding: 15px;
		/* 内边距 */
		margin-bottom: 20px;
		/* 底部间距 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		/* 阴影效果 */
	}

	/* =========================
     学生提交记录部分样式
  ========================= */
	.student-submissions {
		background-color: rgba(249, 249, 249, 0.5);
		/* 背景颜色 */
		border: 1px solid #ddd;
		/* 边框 */
		border-radius: 5px;
		/* 圆角 */
		padding: 15px;
		/* 内边距 */
		margin-bottom: 20px;
		/* 底部间距 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		/* 阴影效果 */
	}


	/* =========================
     下拉框和输入框样式
  ========================= */
	select,
	input[type="text"],
	input[type="datetime-local"],
	textarea,
	input[type="file"] {
		padding: 8px;
		border-radius: 5px;
		border: 1px solid #ced4da;
		background-color: #fff;
		color: #495057;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
		margin-left: 5px;
		margin-right: 5px;
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

	/* =========================
     按钮样式
  ========================= */
	button {
		padding: 8px 10px;
		border-radius: 5px;
		border: none;
		background: rgb(255, 255, 255);
		color: black;
		font-weight: bold;
		font-size: 12px;
		/* 调整字体大小 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		cursor: pointer;
		transition: all 0.3s ease;
		margin-right: 5px;
		/* 按钮间距 */
		margin-left: 5px;
	}


	.pagination {
		display: flex;
		justify-content: center;
		align-items: center;
		/* 确保按钮和文本垂直居中 */
		margin: 20px 0;
		/* 添加上下间距 */
		font-size: 12px;
		/* 调整字体大小 */
	}

	.pagination button {
		padding: 4px 8px;
		/* 调整内边距 */
		font-size: 12px;
		/* 调整字体大小 */
		margin: 0 20px;
		/* 调整按钮间距 */
		border-radius: 3px;
		/* 圆角效果 */
		background-color: #f0f0f0;
		/* 背景颜色 */
		cursor: pointer;
		/* 鼠标悬停效果 */
		transition: background-color 0.3s;
		/* 平滑过渡 */
	}

	.pagination button:hover {
		background-color: #e0e0e0;
		/* 鼠标悬停效果 */
	}

	.pagination button:disabled {
		background-color: #ccc;
		/* 禁用状态背景颜色 */
		cursor: not-allowed;
		/* 禁用状态光标 */
	}

	.action-buttons {
		display: flex;

		margin-top: 20px;
		/* 添加顶部间距 */
		margin-top: auto;
	}

	.exercise-container {
		display: flex;
		justify-content: space-between;
		margin-bottom: 20px;
	}

	.exercise-upload,
	.knowledge-base {
		flex: 1;
		/* 使两个部分等宽 */
		margin-right: 10px;
		/* 右侧间距，避免重叠 */
	}

	.exercise-upload:last-child,
	.knowledge-base:last-child {
		margin-right: 0;
		/* 最后一个元素不需要右边距 */
	}
</style>