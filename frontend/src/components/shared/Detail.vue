<template>
    <div class="resource-detail">
      <h2>{{ resource.name }} 详情</h2>
      <p><strong>上传时间:</strong> {{ resource.uploadTime }}</p>
      <p><strong>描述:</strong> {{ resource.description }}</p>
      <button @click="closeDetail">关闭</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      resource: Object,
    },
    methods: {
      closeDetail() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style >
  .resource-detail {
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  </style>