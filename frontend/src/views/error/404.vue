<template>
  <div class="error-page">
    <div class="error-content">
      <h1 class="error-code">404</h1>
      <h2 class="error-message">页面找不到了</h2>
      <p class="error-desc">您访问的页面不存在或已被移动</p>
      <div class="error-actions">
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button @click="goBack">返回上页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.error-page {
  width: 100vw;
  height: 100vh;
  background: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-content {
  text-align: center;
}

.error-code {
  font-size: 120px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 20px;
  text-shadow: 2px 4px 6px rgba(0, 0, 0, 0.1);
}

.error-message {
  font-size: 32px;
  color: #333;
  margin-bottom: 16px;
}

.error-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>
