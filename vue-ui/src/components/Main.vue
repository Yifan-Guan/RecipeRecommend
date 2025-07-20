<template>
    <n-flex 
    justify="space-between"
    class="top-bar">
        <n-space>
        <n-tabs 
        type="line"
        animated
        @update:value="handleTabChange"
        >
        <n-tab name="home">首页</n-tab>
        <n-tab name="chat">聊天</n-tab>
        <n-tab name="recipe">菜谱</n-tab>
        <n-tab name="recommend">推荐</n-tab>
        <n-tab name="tool">工具</n-tab>
        <n-tab name="about">关于</n-tab>
        </n-tabs>
        </n-space>
        <n-space>
        <n-avatar round
        class="user-avatar">
            U
        </n-avatar>
        <n-button ghost 
            type="primary"
            @click="showLoginModal = true"
            >
        注册/登录
        </n-button>
        <n-modal
        :show="showLoginModal"
        >
          <Login
          :close-login-modal="closeLoginModal"
          ></Login>
        </n-modal>
        </n-space>
    </n-flex>
    <n-divider vertical/>
    <router-view></router-view>
</template>

<script lang="ts"> export default {name: "Main"}</script>
<script setup lang="ts">
import { NSpace, NDivider, NAvatar, NButton, NFlex, NTabs, NTab} from 'naive-ui';
import {NModal} from 'naive-ui';
import {ref} from 'vue';
import {useRouter} from 'vue-router'
import Login from '@/components/Login.vue'

let showLoginModal = ref(false)
const router = useRouter();

function handleTabChange(value: string) {
  router.push({ name: value });
}

function closeLoginModal() {
  showLoginModal.value = false;
  console.log("Login modal closed");
}
</script>

<style scoped>
.top-bar {
    padding: 20px;
}
.user-avatar {
    color: yellow;
    background-color: red;
}
</style>