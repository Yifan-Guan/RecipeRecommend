<template>
  <NConfigProvider
  :locale="zhCN"
  :data-local="dateZhCN"
  >
  <chatWindow/>
  </NConfigProvider>
</template>

<script lang="ts"> export default {name: "App"}</script>
<script setup lang="ts">
import { NConfigProvider, zhCN, dateZhCN } from 'naive-ui';
import ChatWindow from '@/components/ChatWindow.vue'

</script>


<style scoped>
.app-title {
  font-size: 40px;
  text-align: center;
}
</style>
