<template>
  <div class = "app">
    <h1 class="app-title">Recipe Recommend</h1>
    <ChatWindow/>
  </div>
</template>

<script lang="ts"> export default {name: "App"}</script>
<script setup lang="ts">
import ChatWindow from '@/components/ChatWindow.vue'

</script>


<style scoped>
.app-title {
  font-size: 40px;
  text-align: center;
}
</style>
