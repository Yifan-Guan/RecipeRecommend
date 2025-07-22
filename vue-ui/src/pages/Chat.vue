<template>
  <n-flex style="height: 80vh; width: 100vw;">
  <n-layout-sider
        bordered
        :width="240"
        :native-scrollbar="false"
        class="chat-sidebar"
      >
        <!-- 创建新对话按钮 -->
        <div style="padding: 12px;">
          <n-button block
            type="primary"
            @click="createNewChat"
            style="height: 40px;"
          >
            <n-icon size="18" style="margin-right: 8px;">
              <Add />
            </n-icon>
            新建对话
          </n-button>
        </div>

        <!-- 历史记录列表 -->
        <div style="flex: 1; overflow-y: auto; padding: 0 12px;">
          <n-scrollbar style="max-height: 100%;">
            <div 
              v-for="(history) in chatHistory"
              :key="nanoid()"
              class="history-item"
              :class="{ active: currentChatId === history.id }"
              @click="loadChatHistory(history.id)"
            >
              <n-icon size="16" style="margin-right: 8px;">
                <ChatbubbleEllipses />
              </n-icon>
              <span class="history-title">{{ history.title }}</span>
              <n-button text
                style="margin-left: auto;"
                @click.stop="deleteHistory(history.id)"
              >
                <n-icon size="16">
                  <Close />
                </n-icon>
              </n-button>
            </div>
          </n-scrollbar>
        </div>

        <!-- 底部用户设置 -->
        <div style="padding: 12px; border-top: 1px solid #eee;">
          <n-button text block style="justify-content: flex-start;">
            <n-icon size="18" style="margin-right: 8px;">
              <Settings />
            </n-icon>
            设置
          </n-button>
        </div>
  </n-layout-sider>

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
          <n-icon style="margin-left: 8px;">
            <Send />
          </n-icon>
        </n-button>
      </n-input-group>
    </div>
  </n-flex>
  </n-flex>
</template>


<script lang="ts">export default {name: "Chat"}</script>
<script setup lang="ts">
import { ref, reactive, nextTick } from 'vue'
import { 
  NIcon, NInputGroup, NFlex, NButton, NInput, NScrollbar, NLayoutSider, NSpace,
} from 'naive-ui'
import { 
  Add, Send, ChatbubbleEllipses, Settings, Close 
} from '@vicons/ionicons5'
import { nanoid } from 'nanoid'
import { type ChatMessage, type ChatHistory } from '@/types'
import { sendMessageToOpenAI, getContentFromOpenAIResponse } from '@/hooks/chat-with-openai'

// 数据
const currentUserMessage = ref('')
const scrollbarRef = ref()
const currentChatId = ref('')
const messagesList = reactive<ChatMessage[]>([])
const chatHistory = reactive<ChatHistory[]>([
  { id: '1', title: '如何学习Vue3', messages: [{ role: 'assistant', content: 'Vue3学习建议...' }] },
  { id: '2', title: 'Python基础问题', messages: [{ role: 'assistant', content: 'Python入门指南...' }] },
  { id: '3', title: '项目架构讨论', messages: [{ role: 'assistant', content: '关于架构设计的建议...' }] }
])

// 创建新对话
const createNewChat = () => {
  const newId = Date.now().toString()
  currentChatId.value = newId
  messagesList.length = 0
  messagesList.push({ 
    role: 'agent', 
    content: '我是AI助手，请问有什么可以帮助您？' 
  })
  chatHistory.unshift({
    id: newId,
    title: '新对话',
    messages: [...messagesList]
  })
}

// 加载历史记录
const loadChatHistory = (id: string) => {
  currentChatId.value = id
  const history = chatHistory.find(item => item.id === id)
  if (history) {
    messagesList.length = 0
    messagesList.push(...history.messages)
  }
}

// 删除历史记录
const deleteHistory = (id: string) => {
  const index = chatHistory.findIndex(item => item.id === id)
  if (index !== -1) {
    chatHistory.splice(index, 1)
    if (currentChatId.value === id) {
      createNewChat()
    }
  }
}

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

    const currentHistory = chatHistory.find(item => item.id === currentChatId.value)
    if (currentHistory) {
    currentHistory.messages = [...messagesList]
    // 自动生成标题（取第一条用户消息的前20个字符）
      if (messagesList.length >= 2) {
        const firstUserMessage = messagesList.find(m => m.role === 'user')
        if (firstUserMessage) {
          currentHistory.title = firstUserMessage.content.slice(0, 20) + (firstUserMessage.content.length > 20 ? '...' : '')
        }
      }
    }
  }
}

</script>

<style scoped>
.chat-sidebar {
  background: #f7f7f8;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.history-item:hover {
  background: #ededed;
}

.history-item.active {
  background: #e6f4ff;
}

.history-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
}

.chat-container {
  flex: 1;
  height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: white;
  padding: 16px;
  box-sizing: border-box;
  width: 100%;
}

.message-view {
  flex: 1;
  overflow: hidden;
  margin-bottom: 12px;
}

.message-scroll {
  height: 80%;
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
  margin-right: 20px;
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
