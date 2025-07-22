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
import { ref, reactive, nextTick, onMounted, watch} from 'vue'
import { 
  NIcon, NInputGroup, NFlex, NButton, NInput, NScrollbar, NLayoutSider,
} from 'naive-ui'
import { 
  Add, Send, ChatbubbleEllipses, Settings, Close 
} from '@vicons/ionicons5'
import { nanoid } from 'nanoid'
import { 
  type ChatMessage, 
  type ChatHistory,
  type ChatHistoryInfo, 
  type ChatHistoryContent 
} from '@/types'
import { sendMessageToOpenAI, getContentFromOpenAIResponse } from '@/hooks/chat-with-openai'
import {
  fetchChatHistoryInfo,
  fetchChatHistoryContentById,
  addChatHistoryInfo,
  addChatHistoryContent,
  deleteChatHistoryInfo,
  updateChatHistoryNameById
} from '@/hooks/history-manage'
import { useUserInfoStore } from '@/stores/user-info-store'
import { storeToRefs } from 'pinia'

// 数据
const { isLoggedIn, currentUser} = storeToRefs(useUserInfoStore())
const currentUserMessage = ref('')
const scrollbarRef = ref()
const currentChatId = ref('')
const messagesList = reactive<ChatMessage[]>([])
const chatHistory = reactive<ChatHistory[]>([])

onMounted(async () => {
  // 初始化加载历史记录
  if (isLoggedIn.value && currentUser.value) {
    await loadChatHistoryList()
  }
  // 创建默认对话
  createNewChat()
})

// 监听用户登录状态和当前用户变化
watch([isLoggedIn, currentUser], async ([newIsLoggedIn, newCurrentUser], [oldIsLoggedIn, oldCurrentUser]) => {
  // 用户刚登录或切换用户时加载聊天历史
  if (newIsLoggedIn && newCurrentUser && (!oldIsLoggedIn || newCurrentUser?.id !== oldCurrentUser?.id)) {
    // 清空当前聊天历史
    chatHistory.length = 0
    await loadChatHistoryList()
    createNewChat()
  }
}, { deep: true })

async function loadChatHistoryList() {
  // 检查用户是否已登录
  if (!isLoggedIn.value || !currentUser.value?.id) {
    console.log('用户未登录，跳过加载聊天历史')
    return
  }

  try {
    const historyInfoList = await fetchChatHistoryInfo()
    if (historyInfoList) {
      for (const info of historyInfoList) {
        if (info[2] === currentUser.value.id) {
          const historyItem = {
            id: info[0],
            title: info[1],
            messages: [] as ChatMessage[]
          }
          
          const content = await fetchChatHistoryContentById(info[0])
          if (content) {
            content.forEach((msg: [string, string, string, string]) => {
              historyItem.messages.push({
                id: msg[1],
                role: msg[2],
                content: msg[3]
              })
            })
          }
          
          chatHistory.push(historyItem)
        }
      }
      console.log(`加载了 ${chatHistory.length} 条聊天历史记录`)
    }
  } catch (error) {
    console.error('加载聊天历史失败:', error)
  }
}
// 创建新对话
async function createNewChat() {
  const newId = Date.now().toString()
  currentChatId.value = newId
  messagesList.length = 0
  messagesList.push({ 
    id: messagesList.length.toString(),
    role: 'agent', 
    content: '我是AI助手，请问有什么可以帮助您？' 
  })
  chatHistory.unshift({
    id: newId,
    title: '新对话',
    messages: [...messagesList]
  })
  await addChatHistoryInfo(<ChatHistoryInfo>{
    id: newId,
    title: '新对话',
    userId: currentUser.value?.id
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
async function deleteHistory(id: string) {
  const index = chatHistory.findIndex(item => item.id === id)
  if (index !== -1) {
    chatHistory.splice(index, 1)
    if (currentChatId.value === id) {
      createNewChat()
    }
  }
  await deleteChatHistoryInfo(id)
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
      id: messagesList.length.toString(),
      role: "user",
      content: sendMessage
    });
    scrollToBottom()

    messagesList.push({
      id: messagesList.length.toString(),
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
    await addChatHistoryContent(<ChatHistoryContent>{
      id: currentChatId.value,
      index: (messagesList.length - 2),
      role: messagesList[messagesList.length - 2].role,
      content: messagesList[messagesList.length - 2].content,
    })
    await addChatHistoryContent(<ChatHistoryContent>{
      id: currentChatId.value,
      index: (messagesList.length - 1),
      role: messagesList[messagesList.length - 1].role,
      content: messagesList[messagesList.length - 1].content,
    })


    const currentHistory = chatHistory.find(item => item.id === currentChatId.value)
    if (currentHistory) {
    currentHistory.messages = [...messagesList]
    // 自动生成标题（取第一条用户消息的前20个字符）
      if (messagesList.length >= 2) {
        const firstUserMessage = messagesList.find(m => m.role === 'user')
        if (firstUserMessage) {
          currentHistory.title = firstUserMessage.content.slice(0, 20) + (firstUserMessage.content.length > 20 ? '...' : '')
          await updateChatHistoryNameById(currentHistory.id, currentHistory.title)
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
