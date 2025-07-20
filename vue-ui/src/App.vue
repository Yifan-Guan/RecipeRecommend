<template>
  <NConfigProvider
  :locale="zhCN"
  :data-local="dateZhCN"
  >
    <Main/>
  </NConfigProvider>
</template>

<script lang="ts"> export default {name: "App"}</script>
<script setup lang="ts">
import { NConfigProvider, zhCN, dateZhCN, NSpace, NDivider} from 'naive-ui';
import Main from '@/components/Main.vue';
</script>


<style scoped>
</style>
