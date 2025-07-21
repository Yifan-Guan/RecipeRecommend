<template>
  <n-flex vertical class="chat-container">
    <div class="message-view">
      <n-scrollbar ref="scrollbarRef" class="message-scroll">
        <div class="message-list">
          <div
            v-for="(message, index) in messagesList"
            :key="index"
            :class="['chat-bubble', message.role === 'user' ? 'user' : 'agent']"
          >
            <div class="chat-name">
              {{ message.role === 'user' ? '我' : 'AI 助手' }}
            </div>
            <div class="chat-content">
              {{ message.content }}
            </div>
          </div>
        </div>
      </n-scrollbar>
    </div>

    <div class="chat-input-area">
      <n-input-group class="chat-input-group">
        <n-input
          round
          type="textarea"
          placeholder="请输入您的问题"
          v-model:value="currentUserMessage"
          :autosize="{ maxRows: 5 }"
          @keyup.enter="sendUserMessage"
          class="chat-input"
        />
        <n-button
          ghost
          round
          type="primary"
          @click="sendUserMessage"
          class="chat-send-button"
        >
          Send
        </n-button>
      </n-input-group>
    </div>
  </n-flex>
</template>


<script lang="ts">
export default {
  name: "Chat"
}
</script>

<script setup lang="ts">
import { NCard, NInputGroup, NFlex, NButton, NInput, NScrollbar } from 'naive-ui'
import { ref, reactive, nextTick } from 'vue'
import { nanoid } from 'nanoid'
import { type ChatMessage } from '@/types'
import { sendMessageToOpenAI, getContentFromOpenAIResponse } from '@/hooks/chat-with-openai'

let currentUserMessage = ref("")
let scrollbarRef = ref()
let messagesList: Array<ChatMessage> = reactive([
  {
    role: "agent",
    content: "Hello! How can I assist you today?"
  }
])

function scrollToBottom() {
  nextTick(() => {
    const scrollbar = scrollbarRef.value
    if (scrollbar?.scrollTo) {
      scrollbar.scrollTo({
        top: Number.MAX_SAFE_INTEGER,  
        behavior: 'smooth'
      })
    }
  })
}


async function sendUserMessage() {
  if (currentUserMessage.value.trim()) {
    let sendMessage = currentUserMessage.value
    currentUserMessage.value = ""
    messagesList.push({
      role: "user",
      content: sendMessage
    });
    scrollToBottom()

    messagesList.push({
      role: "agent",
      content: "正在思考中..."
    });
    scrollToBottom()

    let agentResponse = await sendMessageToOpenAI(sendMessage)
    if (agentResponse) {
      await getContentFromOpenAIResponse(agentResponse, messagesList)
      scrollToBottom()
    } else {
      messagesList[messagesList.length - 1].content = "请求失败，请稍后再试"
      scrollToBottom()
    }
  }
}
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: white;
  padding: 16px;
  box-sizing: border-box;
  max-width: 1200px;
  margin: 0 auto;
}

.message-view {
  flex: 1;
  overflow: hidden;
  margin-bottom: 12px;
}

.message-scroll {
  height: 100%;
  padding: 8px 16px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  display: flex;
  flex-direction: column;
}

.chat-bubble.agent {
  align-self: flex-start;
  background-color: #e9f5ff;
  color: #333;
}

.chat-bubble.user {
  align-self: flex-end;
  background-color: #d1f2eb;
  color: #111;
}

.chat-name {
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #666;
}

.chat-bubble.agent .chat-name {
  text-align: left;
  color: #0077cc;
}

.chat-bubble.user .chat-name {
  text-align: right;
  color: #00aa88;
}

.chat-content {
  white-space: pre-wrap;
}

.chat-input-area {
  padding: 8px 0;
  border-top: 1px solid #ddd;
}

.chat-input-group {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.chat-input {
  flex: 1;
}

.chat-send-button {
  flex-shrink: 0;
}
</style>
