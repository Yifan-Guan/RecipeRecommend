<template>
    <n-card  
    class="login-card">
    <n-tabs
      class="card-tabs"
      default-value="signin"
      size="large"
      animated
      pane-wrapper-style="margin: 0 -4px"
      pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
    >
      <n-tab-pane name="signin" tab="登录">
        <n-form :model="logInUserModel" :rules="loginUserRules">
          <n-form-item-row label="用户名" path="logInUserName">
            <n-input 
            type="text"
            v-model:value="logInUserModel.logInUserName" />
          </n-form-item-row>
          <n-form-item-row label="密码" path="logInPassword">
            <n-input 
            type="password"
            v-model:value="logInUserModel.logInPassword" />
          </n-form-item-row>
        </n-form>
        <n-button type="primary" block secondary strong
        @click="signIn()">
          登录
        </n-button>
        <n-button block secondary strong 
        :style="{ marginTop: '10px' }"
        @click="closeLoginModal()">
          取消
        </n-button>
      </n-tab-pane>
      <n-tab-pane name="signup" tab="注册">
        <n-form :model="signUpUserModel">
          <n-form-item-row label="用户名">
            <n-input v-model:value="signUpUserModel.signUpUserName" />
          </n-form-item-row>
          <n-form-item-row label="密码">
            <n-input v-model:value="signUpUserModel.signUpPassword" />
          </n-form-item-row>
          <n-form-item-row label="重复密码">
            <n-input v-model:value="signUpUserModel.signUpConfirmPassword" />
          </n-form-item-row>
        </n-form>
        <n-button type="primary" block secondary strong>
          注册
        </n-button>
        <n-button block secondary strong 
        :style="{ marginTop: '10px' }"
        @click="closeLoginModal()">
          取消
        </n-button>
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script lang="ts"> export default {name: "Login"}</script>
<script setup lang="ts">
import { NCard, NTabs, NTabPane, NForm, NFormItemRow, NInput, NButton } from 'naive-ui'
import {ref, reactive} from 'vue';
import { useUserInfoStore } from '@/stores/user-info-store';

let {closeLoginModal}= defineProps(['closeLoginModal']);

const userInfoStore = useUserInfoStore();

let logInUserModel = reactive({
  logInUserName: '',
  logInPassword: ''
});

let loginUserRules = {
  logInUserName: [
    { required: true, message: '用户名', trigger: 'blur' }
  ],
  logInPassword: [
    { required: true, message: '密码', trigger: 'blur' }
  ]
};

let signUpUserModel = reactive({
  signUpUserName: '',
  signUpPassword: '',
  signUpConfirmPassword: ''
});

function signIn() {
  let result = userInfoStore.logIn({
    name: logInUserModel.logInUserName,
    password: logInUserModel.logInPassword
  });
  if (result) {
    closeLoginModal();
  } else {
  }
}
</script>

<style scoped>
.login-card {
  width: 400px
}
</style>