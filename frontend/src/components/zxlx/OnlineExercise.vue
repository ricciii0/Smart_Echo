<template>
	<div class="main-container">
		<Sidebar />
		<router-view />

		<div class="main-content">
			<UserControls :username="username" v-model="selectedClass" @logout="handleLogout" />

			<div class="content-area">
				<div class="exercise-container">
					<div class="exercise-upload">
						<h3>上传练习</h3>
						<input type="file" ref="upload_file">
						<input type="text" v-model="exercisetitle" placeholder="练习标题" />
						<button @click="uploadExercise">上传练习题</button>
					</div>

					<div class="knowledge-base">
						<h3>从知识库选择题目</h3>
						<select v-model="selectedKnowledgeQuestion">
							<option v-for="question in knowledgeBase" :key="question.id" :value="question.id">
								{{ question.name }}
							</option>
						</select>
						<input type="text" v-model="exercisetitle2" placeholder="练习标题" />
						<button @click="addToExercises">添加到练习</button>
					</div>
				</div>

				<div class="student-submissions">
					<h3>查看学生提交记录</h3>
					<div class="search-bar">
						<input type="text" v-model="searchName" placeholder="输入练习内容" />
						<button @click="performSearch">搜索</button>
						<button @click="refresh">刷新</button>
					</div>
					<table class="submission-table">
						<thead>
							<tr>
								<th>序号</th>
								<th>学生姓名</th>
								<th>标题</th>
								<th>提交时间</th>
								<th>分数</th>
								<th>批改时间</th>
								<th>操作</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(record, index) in historyRecords" :key="index">
								<td>{{ index + 1 }}</td>
								<td>{{ record.studentName }}</td>
								<td>{{ record.title }}</td>
								<td>{{ record.submitTime }}</td>
								<td>{{ record.grade }}</td>
								<td>{{ record.correcttime}}</td>
								<td>
									<button @click="viewSubmission(record)">查看详情</button>


									<!-- 按钮触发弹窗 -->
									<button @click="dialogVisible = true" class="open-dialog-btn">批改</button>

									<!-- 使用 teleport 将弹窗渲染到 body 中 -->
									<teleport to="body">
										<div v-if="dialogVisible" class="dialog-overlay">
											<div class="dialog">
												<h3>批改</h3>

												<form @submit.prevent="submitForm(record)">
													<!-- 得分输入框 -->
													<div class="form-group">
														<label for="score">得分：</label>
														<input type="number" v-model="form.score" id="score"
															placeholder="请输入得分" />
													</div>

													<!-- 老师评价多行输入框 -->
													<div class="form-group">
														<label for="comments">老师评价：</label>
														<textarea v-model="form.comments" id="comments" rows="4"
															placeholder="请输入老师评价"></textarea>
													</div>

													<!-- 按钮部分 -->
													<div class="dialog-footer">
														<button type="button" @click="dialogVisible = false"
															class="cancel-btn">取消</button>
														<button type="submit" class="submit-btn">提交</button>
													</div>
												</form>
											</div>
										</div>
									</teleport>

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
					<div class="action-buttons">
						<button @click="exportProgress">导出练习完成情况</button>
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
				username: 'admin',
				selectedClass: '班级2',
				selectedKnowledgeQuestion: null,
				selectedSubmission: null,
				knowledgeBase: [{
						"name": "练习一",
						"id": 1,
					},
					{
						"name": "练习二",
						"id": 2,
					},
				], // 假设知识库数据
				historyRecords: [{
					studentName: "加载中",
					title: "加载中",
					submitTime: "加载中",
					grade: "加载中",
					correcttime: "加载中",
				}, ], // 假设提交记录数据
				selectedRecord: null, // 当前查看的提交记录
				searchName: '', // 学生姓名
				searchDate: '', // 提交日期
				filteredRecords: [], // 存储搜索结果
				score: '',
				feedback: '',

				exercisetitle: '',
				exercisetitle2: '',

				dialogVisible: false,
				form: {
					score: '',
					comments: '',
				},
			};
		},
		mounted() {
			this.getRecord();
			this.getKnowledgeRecords();
		},

		methods: {
			getKnowledgeRecords() {
				let teaid = 0;
				axios.get('http://127.0.0.1:5000/rm/printdb/', {
						params: {
							teaid: teaid
						}
					})
					.then(result => {
						this.knowledgeBase = result.data;
					});
			},
			addToExercises() {
				if (this.selectedKnowledgeQuestion != null && this.exercisetitle2) {
					// 进行文件上传的操作,const用作创建一个常量的变量，new是创建出来一个新的对象
					const formData = new FormData();
					formData.append('targetclass', this.selectedClass);
					formData.append('title', this.exercisetitle2);
					// 因为我还不会使用去获取教师的id或者名字，所以这里就随便设置了
					let teacherid = 0;
					//这里假如获得了学生的id列表
					let studentid_s = [2, 3, 4, 5, 6, 7, 8];
					let studentidString = studentid_s.join(',');
					formData.append('studentid_s', studentidString);
					// 到时候这里需要修改的
					formData.append('teacherid', teacherid);
					formData.append('exeid', this.selectedKnowledgeQuestion);
					// 使用 axios 进行上传
					axios.post('http://127.0.0.1:5000/oe/uploadfromdb/', formData, {
							headers: {
								'Content-Type': 'multipart/form-data'
							},
						})
						.then(response => {
							alert('成功上传文件', response.data);
						})
						.catch(error => {
							alert('文件上传失败', error);
						});
				} else if (this.selectedKnowledgeQuestion == null) {
					alert('管理员梁耀欣提示您：没有从知识库中选择练习');
				} else {
					alert('管理员梁耀欣提示您：没有指定标题');
				}
			},
			getRecord() {
				let teaid = 0;
				axios.post('http://127.0.0.1:5000/oe/tearecord/', {
						id: teaid
					})
					.then(result => {
						this.historyRecords = result.data;
					});
			},
			refresh() {
				this.$router.go(0);
			},

			// viewSubmission(record) {
			// 	axios({
			// 			url: `http://127.0.0.1:5000/oe/viewsubmission/`,
			// 			method: 'POST',
			// 			data: {
			// 				record
			// 			}, //使用POST方式将 id 作为请求体的一部分
			// 			responseType: 'blob' // 指定响应类型为 Blob
			// 		})
			// 		.then(response => {
			// 			const url = window.URL.createObjectURL(new Blob([response.data]));
			// 			const a = document.createElement('a');
			// 			a.href = url;
			// 			a.download = record.answername;
			// 			document.body.appendChild(a);
			// 			a.click();
			// 			document.body.removeChild(a);
			// 		})
			// 		.catch(error => {
			// 			console.error('Error:', error);
			// 		});
			// },

			viewSubmission(record) {
				// 打开新窗口预览文件
				window.open(`http://127.0.0.1:5000/oe/preview_material/${record.id}`, '_blank');
			},



			performSearch() {
				alert(this.searchName)
				if (this.searchName) {
					const lowerQuery = this.searchName.toLowerCase();
					// alert(lowerQuery);
					for (let i = 0; i < this.historyRecords.length; i++) {
						// 这里面的学生姓名由于不是字符串，所以无法进行这样的检索
						if (!(this.historyRecords[i].title.toLowerCase().includes(lowerQuery))) {
							//从i开始删除一个元素
							this.historyRecords.splice(i, 1);
							i--;
						}
					}
				}
			},
			logout() {
				alert('已退出登录');
				this.$router.push('/');
			},
			uploadExercise() {
				// 通过 this.$refs 访问文件输入框
				const fileInput = this.$refs.upload_file;
				const file = fileInput.files[0]; // 获取用户选择的文件
				if (file && this.exercisetitle) {
					// 进行文件上传的操作,const用作创建一个常量的变量，new是创建出来一个新的对象
					const formData = new FormData();
					formData.append('file', file);
					formData.append('targetclass', this.selectedClass);
					formData.append('title', this.exercisetitle);
					// 因为我还不会使用去获取教师的id或者名字，所以这里就随便设置了
					let teacherid = 0;
					//这里假如获得了学生的id列表
					let studentid_s = [2, 3, 4, 5, 6, 7, 8];
					let studentidString = studentid_s.join(',');
					formData.append('studentid_s', studentidString);
					// 到时候这里需要修改的
					formData.append('teacherid', teacherid);
					// 使用 axios 进行上传
					axios.post('http://127.0.0.1:5000/oe/upload/', formData, {
							headers: {
								'Content-Type': 'multipart/form-data'
							},
						})
						.then(response => {
							alert('成功上传文件:', response.data);
						})
						.catch(error => {
							alert('文件上传失败:', error);
						});
				} else if (!file) {
					alert('管理员梁耀欣提示您：没有选择文件');
				} else {
					alert('管理员梁耀欣提示您：没有指定标题');
				}
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


			submitFeedback() {
				if (this.selectedRecord) {
					this.selectedRecord.score = this.score;
					this.selectedRecord.feedback = this.feedback;
					alert('反馈已提交');
					this.score = '';
					this.feedback = '';
				}
			},
			exportProgress() {
				const data = this.historyRecords.map(record => ({
					id: record.id,
					studentName: record.studentName,
					title: record.title,
					submitTime: record.submitTime,
					correcttime: record.correcttime,
					grade: record.grade,
					feedback: record.feedback,
				}));

				const csvContent = this.convertToCSV(data);
				const blob = new Blob([csvContent], {
					type: 'text/csv;charset=utf-8;'
				});
				const url = URL.createObjectURL(blob);
				const link = document.createElement('a');
				link.setAttribute('href', url);
				link.setAttribute('download', 'exercise_progress.csv');
				link.style.visibility = 'hidden';
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			},

			convertToCSV(data) {
				const header = Object.keys(data[0]).join(',') + '\n';
				const rows = data.map(row => Object.values(row).join(',')).join('\n');
				return header + rows;
			},

			submitForm(record) {


				const formData = new FormData();
				formData.append('aimid', record['id']);
				formData.append('score', this.form.score);
				formData.append('comments', this.form.comments);

				axios.post('http://127.0.0.1:5000/oe/correct/', formData, {
						headers: {
							'Content-Type': 'multipart/form-data'
						},
					})
					.then(response => {
						alert('成功上传得分', response.data);
					})
					.catch(error => {
						alert('得分上传失败:', error);
					});

				this.dialogVisible = false; // 提交后关闭弹窗
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
		background-image: url('../../img/background.png');
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
		height: 500px;
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

	input[type="text"] {
		padding: 8px;
		border-radius: 5px;
		border: 1px solid #ced4da;
		background-color: #fff;
		color: #495057;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
		width: 140px;
		/* 设置你需要的宽度 */
	}

	select,
	input[type="datetime-local"],
	textarea,
	input[type="file"],
	input[type="date"] {
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


	/* 弹窗背景遮罩 */
	.dialog-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
		/* 确保弹窗位于最上层 */
	}

	/* 弹窗样式 */
	.dialog {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		width: 300px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}

	h3 {
		margin-top: 0;
		text-align: center;
	}

	.form-group {
		margin-bottom: 15px;
	}

	label {
		display: block;
		font-weight: bold;
		margin-bottom: 5px;
	}

	input[type="number"],
	textarea {
		width: 100%;
		padding: 8px;
		border: 1px solid #ccc;
		border-radius: 4px;
		font-size: 14px;
	}

	.dialog-footer {
		display: flex;
		justify-content: flex-end;
		gap: 10px;
	}

	button {
		padding: 8px 16px;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.open-dialog-btn {
		background-color: #409EFF;
		color: white;
	}

	.cancel-btn {
		background-color: #F56C6C;
		color: white;
	}

	.submit-btn {
		background-color: #67C23A;
		color: white;
	}
</style>