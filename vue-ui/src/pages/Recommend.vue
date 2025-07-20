<template>
  <n-result status="404" title="Recommend 资源不存在" description="生活总归带点荒谬">
    <template #footer>
      <n-button>找点乐子吧</n-button>
    </template>
  </n-result>
</template>

<script lang="ts"> export default {name: "About"}</script>
<script setup lang="ts">
import {NResult, NButton} from 'naive-ui'
</script>

<style scoped>
</style>