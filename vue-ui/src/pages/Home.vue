<template>
  <div class="home-container">

    <n-image
      class="banner-img"
      src="/logo.png"
      alt="logo"
      width="100%"
      height="300"
      object-fit="cover"
      preview-disabled
    />

    <n-card class="welcome-card" :hoverable="true">
      <h2>欢迎来到 AI 食谱推荐助手</h2>
      <p>输入食材、口味偏好或健康需求，我们将为你推荐最合适的食谱。</p>

      <n-space justify="center" class="entry-buttons">
        <n-button type="primary" @click="goTo('chat')">开始对话</n-button>
        <n-button @click="goTo('recommend')">个性化推荐</n-button>
        <n-button @click="goTo('recipe')">浏览菜谱</n-button>
      </n-space>
    </n-card>

    
  </div>
</template>

<script setup lang="ts">
import { NCard, NSpace, NButton, NImage } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
function goTo(name: string) {
  router.push({ name })
}
</script>

<style scoped>
.home-container {
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}

.welcome-card {
  max-width: 700px;
  text-align: center;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 16px;
}

.entry-buttons {
  margin-top: 20px;
}

.banner-img {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>
