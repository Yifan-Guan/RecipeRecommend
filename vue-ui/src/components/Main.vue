<template>
    <n-flex 
    justify="space-between"
    class="top-bar">
        <n-space>
        <n-tabs 
        type="line"
        v-model:value="router.currentRoute.value.name"
        animated
        @update:value="handleTabChange"
        >
        <n-tab name="home">首页</n-tab>
        <n-tab name="chat">聊天</n-tab>
        <n-tab name="recipe">菜谱</n-tab>
        </n-tabs>
        </n-space>
        <n-space>
        <n-avatar round
        :class="isLoggedIn ? 'logged-in-avatar' : 'guest-avatar'"
        >
            {{ avatarText }}
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
import {ref, watch} from 'vue';
import { storeToRefs } from 'pinia';
import {useRouter} from 'vue-router'
import { useUserInfoStore } from '@/stores/user-info-store';
import Login from '@/components/Login.vue'

let showLoginModal = ref(false)
const {isLoggedIn, currentUser} = storeToRefs(useUserInfoStore());
let avatarText = ref(
  isLoggedIn.value ? currentUser.value?.name?.charAt(0).toUpperCase() : 'G'
)
watch(isLoggedIn, (newVal) => {
  avatarText.value = newVal ? currentUser.value?.name?.charAt(0).toUpperCase() : 'G';
});

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
.guest-avatar {
    color: white;
    background-color: gray;
}
.logged-in-avatar {
    color: white;
    background-color: purple;
}
</style>