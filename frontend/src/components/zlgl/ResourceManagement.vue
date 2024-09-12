<template>
	<div class="main-container">
		<Sidebar />
		<router-view />

		<div class="main-content">
			<UserControls :username="username" v-model="selectedClass" @logout="handleLogout" />

			<div class="content-area">
				<div class="search-bar">
					<input type="text" v-model="resourceName" placeholder="内容" />
					<select v-model="selectedSubject">
						<option value="defaults">科目</option>
						<option value="计算机">计算机</option>
						<option value="数学">数学</option>
						<option value="语文">语文</option>
						<option value="英语">英语</option>
					</select>
					<input type="text" v-model="Timetxt" placeholder="时间" />

					<!-- 触发按钮 -->
					<button @click="openModal" class="open-btn">选择时间范围</button>
					<!-- <div v-if="startTime && endTime" class="selected-time" style="font-size: 10px;">
						选择的时间范围:<br/>
						{{ startTime }} 至 {{ endTime }}
					</div> -->
					<!-- 模态窗口 -->
					<div v-if="isModalOpen" class="modal">
						<div class="modal-content">
							<span class="close" @click="closeModal">&times;</span>
							<h2>请选择时间范围</h2>
							<div class="input-group">
								<label for="start-time">开始时间:</label>
								<input type="datetime-local" v-model="startTime" id="start-time">
							</div>
							<div class="input-group">
								<label for="end-time">结束时间:</label>
								<input type="datetime-local" v-model="endTime" id="end-time">
							</div>
							<button id="unique-button" @click="submitTimeRange">提交</button>
						</div>
					</div>

					<button @click="searchResources">查询</button>
					<button @click="resetFields">刷新</button>
					<button @click="deleteFields">删除选中</button>
					<!-- ref="uploadFile"的作用是让你在React组件中能够通过this.refs.uploadFile访问到该input元素 -->
					<input type="file" ref="upload_file" />
					<select v-model="theSubject">
						<option value="defaults">科目</option>
						<option value="语文">语文</option>
						<option value="数学">数学</option>
						<option value="英语">英语</option>
						<option value="计算机">计算机</option>
					</select>
					<button @click="uploadFile">上传</button>
				</div>

				<table class="resource-table">
					<thead>
						<tr>
							<th>选择</th>
							<th>序号</th>
							<th>资料内容</th>
							<th>学科分类</th>
							<th>上传时间</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(resource, index) in resources" :key="index">
							<td>
								<input type="checkbox" v-model="resource.selected" />
							</td>
							<td>{{ index + 1 }}</td>
							<td>{{ resource.name }}</td>
							<td>{{ resource.subject }}</td>
							<td>{{ resource.uploadTime }}</td>
							<td>
								<button @click="viewResource(resource)">查看</button>
								<button @click="downloadResource(resource)">下载</button>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="pagination">
					<button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
					<span>第 {{ currentPage }} 页</span>
					<button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
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
				isModalOpen: false, // 控制模态窗口的显示与隐藏
				startTime: '', // 存储开始时间
				endTime: '', // 存储结束时间

				Timetxt: '',
				theSubject: 'defaults',

				username: 'admin',
				selectedClass: '班级1',
				resourceName: '',
				selectedSubject: 'defaults',
				resources: [
					// 添加更多示例资源以便于分页
					{
						name: '加载中...',
						uploader: '加载中...',
						subject: '加载中...',
						uploadTime: '加载中...',
						selected: false
					},
				],
				currentPage: 1,
				itemsPerPage: 5, // 每页显示的条数
			};
		},
		mounted() {
			this.getData();
		},
		methods: {
			logout() {
				// 退出登录逻辑
				alert('已退出登录');
				this.$router.push('/');
			},
			searchResources() {
				// 先刷新一下
				// await this.getData()
				if (this.selectedSubject != 'defaults') {
					for (let i = 0; i < this.resources.length; i++) {
						if (this.resources[i].subject != this.selectedSubject) {
							//从i开始删除一个元素
							this.resources.splice(i, 1);
							i--;
						}
					}
				}
				if (this.startTime && this.endTime) {
					// 将不同的时间格式全都转换成一种格式就可以实现查询
					const startDate = new Date(this.startTime);
					const endDate = new Date(this.endTime);
					// console.log(startDate)
					// console.log(endDate)
					for (let i = 0; i < this.resources.length; i++) {
						const uploadDate = new Date(this.resources[i].uploadTime);
						// 将16小时转换为毫秒
						const hoursToAdd = 8;
						const millisecondsToAdd = hoursToAdd * 60 * 60 * 1000;

						// 计算新的时间戳
						const newTimestamp = uploadDate.getTime() - millisecondsToAdd;
						const newDate = new Date(newTimestamp);
						// console.log(this.resources[i].uploadTime)
						// console.log(newDate)

						if (newDate < startDate || newDate > endDate) {
							//从i开始删除一个元素
							this.resources.splice(i, 1);
							i--;
						}
					}
				}
				if (this.resourceName) {
					const lowerQuery = this.resourceName.toLowerCase();
					// alert(lowerQuery);
					for (let i = 0; i < this.resources.length; i++) {
						if (!(this.resources[i].name.toLowerCase().includes(lowerQuery))) {
							//从i开始删除一个元素
							this.resources.splice(i, 1);
							i--;
						}
					}

				}
			},
			resetFields() {
				// this.resourceName = '';
				// this.selectedSubject = '全部';
				// this.selectedUploadTime = '全部';
				// this.$refs.uploadFile.value = ''; // 清空文件选择
				this.getData();
			},
			uploadFile() {
				// 通过 this.$refs 访问文件输入框
				const fileInput = this.$refs.upload_file;
				const file = fileInput.files[0]; // 获取用户选择的文件
				if (file && this.theSubject != 'defaults') {
					// 进行文件上传的操作,const用作创建一个常量的变量，new是创建出来一个新的对象
					const formData = new FormData();
					formData.append('file', file);
					formData.append('subject', this.theSubject);

					let teaid = 0;
					// teaid为当前登录的用户的id
					formData.append('teaid', teaid);
					// 使用 axios 进行上传
					axios.post('http://127.0.0.1:5000/rm/upload/', formData, {
							headers: {
								'Content-Type': 'multipart/form-data'
							},
							// timeout: 60000
						})
						.then(response => {
							alert('成功上传文件:', response.data);
						})
						.catch(error => {
							alert('文件上传失败:', error);
						});
					//this.$router.go(0);
				} else if (!file) {
					alert('管理员梁耀欣提示您：没有选择文件');
				} else {
					alert('管理员梁耀欣提示您：没有指定科目');
				}

			},
			viewResource(resource) {
				// 打开新窗口预览文件
				window.open(`http://127.0.0.1:5000/rm/preview_material/${resource.id}`, '_blank');
			},
			downloadResource(resource) {
				axios({
						url: `http://127.0.0.1:5000/rm/download/`,
						method: 'POST',
						data: {
							resource
						}, //使用POST方式将 id 作为请求体的一部分
						responseType: 'blob' // 指定响应类型为 Blob
					})
					.then(response => {
						const url = window.URL.createObjectURL(new Blob([response.data]));
						const a = document.createElement('a');
						a.href = url;
						a.download = resource.name;
						document.body.appendChild(a);
						a.click();
						document.body.removeChild(a);
					})
					.catch(error => {
						console.error('Error:', error);
					});
			},
			getData() {
				let teaid = 0;
				axios.get('http://127.0.0.1:5000/rm/print/', {
						params: {
							teaid: teaid
						}
					})
					.then(result => {
						this.resources = result.data;
					});
			},
			deleteFields() {
				let selectedIds = [];
				let isNone = true;

				for (let i = 0; i < this.resources.length; i++) {
					if (this.resources[i].selected) {
						//从i开始删除一个元素
						selectedIds.push(this.resources[i].id);
						this.resources.splice(i, 1);
						isNone = false;
						i--;
					}
				}
				console.log(selectedIds)
				if (isNone) {
					alert("你并未选择任何文件");
				} else {
					axios.post('http://127.0.0.1:5000/rm/detele/', {
							values: selectedIds
						})
						// {} 是对象的字面量表示法，表示你要传递的数据结构
						.then(response => {
							alert(`Respone: ${response.data}`);
						});
				}
			},
			openModal() {
				this.isModalOpen = true; // 打开模态窗口
			},
			closeModal() {
				this.isModalOpen = false; // 关闭模态窗口
			},
			submitTimeRange() {
				if (this.startTime && this.endTime) {
					if (this.startTime < this.endTime) {
						this.Timetxt = `${this.startTime}\n~${this.endTime}`
						this.closeModal(); // 提交后关闭模态窗口
					} else {
						alert("请注意开始时间应该在结束时间之前！");
					}
				} else {
					alert("请选择开始时间和结束时间！");
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
		/* 使用边框盒模型 */
		margin: 0;
		padding: 0;
	}

	html,
	body {
		height: 100%;
		/* 确保 html 和 body 高度为 100% */
		margin: 0;
		font-family: 'Arial', sans-serif;
		/* 设置字体 */
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
   主内容样式
========================= */
	.main-content {
		flex: 1;
		padding: 20px;
		display: flex;
		flex-direction: column;
		margin-left: 20px;
		/* 主内容与侧边栏有间距 */
		overflow: auto;
		/* 允许滚动 */
	}

	.user-controls {
		display: flex;
		align-items: center;
		/* 垂直居中对齐 */
	}

	.user-controls span {
		margin-right: 20px;
		/* 添加右边距以分隔元素 */
	}

	.welcome-message {
		margin-left: 10px;
		margin-right: 20px;
		/* 与选择器分开 */
		font-size: 0.9em;
		/* 调整字体大小 */
		color: #34495e;
		/* 设置颜色 */
	}

	.header {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		margin-bottom: 20px;
	}

	/* =========================
   内容区域样式
========================= */
	.content-area {
		display: flex;
		flex-direction: column;
		flex: 1;
		/* 填满剩余空间 */
	}

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
   下拉框和输入框样式
========================= */
	select {
		padding: 8px;
		border-radius: 5px;
		border: 1px solid #ced4da;
		background-color: #fff;
		color: #495057;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
		width: 90px;
		/* 设置你需要的宽度 */
	}

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
		margin-right: 10px;
		/* 按钮间距 */
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

	/* 模态窗口背景 */
	.modal {
		display: flex;
		justify-content: center;
		align-items: center;
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
	}

	/* 模态窗口内容 */
	.modal-content {
		background-color: white;
		padding: 20px;
		border-radius: 10px;
		width: 350px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		position: relative;
	}

	/* 关闭按钮 */
	.close {
		color: #aaa;
		font-size: 28px;
		font-weight: bold;
		position: absolute;
		top: 10px;
		right: 15px;
	}

	.close:hover,
	.close:focus {
		color: black;
		text-decoration: none;
		cursor: pointer;
	}

	/* 表单样式 */
	.input-group {
		margin: 15px 0;
		width: 100%;
		text-align: left;
	}

	.input-group label {
		display: block;
		font-weight: bold;
		margin-bottom: 5px;
	}

	input[type="datetime-local"] {
		width: calc(100% - 2px);
		/* 调整宽度以适应模态窗口 */
		padding: 10px;
		margin-top: 5px;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
	}

	#unique-button {
		padding: 5px 10px;
		font-size: 16px;
		background-color: #008CBA;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		margin-top: 20px;
	}

	/*
	#unique-button:hover {
		background-color: #007bb5;
	} */
</style>