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
        <n-form>
          <n-form-item-row label="用户名">
            <n-input />
          </n-form-item-row>
          <n-form-item-row label="密码">
            <n-input />
          </n-form-item-row>
        </n-form>
        <n-button type="primary" block secondary strong>
          登录
        </n-button>
        <n-button block secondary strong 
        :style="{ marginTop: '10px' }"
        @click="closeLoginModal()">
          取消
        </n-button>
      </n-tab-pane>
      <n-tab-pane name="signup" tab="注册">
        <n-form>
          <n-form-item-row label="用户名">
            <n-input />
          </n-form-item-row>
          <n-form-item-row label="密码">
            <n-input />
          </n-form-item-row>
          <n-form-item-row label="重复密码">
            <n-input />
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
let {closeLoginModal}= defineProps(['closeLoginModal']);
</script>

<style scoped>
.login-card {
  width: 400px
}
</style>