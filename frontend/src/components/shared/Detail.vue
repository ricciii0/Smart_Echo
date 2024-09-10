<template>
  <div class="resource-detail" v-if="resource">
    <h2>{{ resource.name }} 详情</h2>
    <p><strong>上传时间:</strong> {{ resource.uploadTime }}</p>
    <p><strong>描述:</strong> {{ resource.description }}</p>
    <button @click="closeDetail">关闭</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    resourceId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      resource: null,
    };
  },
  created() {
    this.fetchResourceDetail();
  },
  methods: {
    async fetchResourceDetail() {
      try {
        const response = await axios.get(`/api/resources/${this.resourceId}`);
        this.resource = response.data;
      } catch (error) {
        console.error('获取资源详情失败:', error);
      }
    },
    closeDetail() {
      this.$emit('close');
    },
  },
};
</script>

<style>
.resource-detail {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
</style>
