<template>
  <NConfigProvider
  :locale="zhCN"
  :data-local="dateZhCN"
  :theme-overrides="ThemeOverrides"
  >
    <Main/>
  </NConfigProvider>
</template>

<script lang="ts"> export default {name: "App"}</script>
<script setup lang="ts">
import { NConfigProvider, zhCN, dateZhCN, NSpace, NDivider} from 'naive-ui';
import ThemeOverrides from '@/theme.ts'
import Main from '@/components/Main.vue';
</script>


<style scoped>
</style>
