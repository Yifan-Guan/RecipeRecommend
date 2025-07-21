<template>
  <div class="full-container">
    <n-layout has-sider style="height: 100vh">
      <!-- 侧边栏 - 参考DeepSeek设计 -->
      <n-layout-sider
        bordered
        :width="240"
        :native-scrollbar="false"
        content-style="
          display: flex;
          flex-direction: column;
          height: 100%;
          background: #f7f7f8;
        "
      >
        <!-- 创建新对话按钮 -->
        <div style="padding: 12px;">
          <n-button
            block
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
              v-for="(history, index) in chatHistory"
              :key="index"
              class="history-item"
              :class="{ active: currentChatId === history.id }"
              @click="loadChatHistory(history.id)"
            >
              <n-icon size="16" style="margin-right: 8px;">
                <ChatbubbleEllipses />
              </n-icon>
              <span class="history-title">{{ history.title }}</span>
              <n-button
                text
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

      <!-- 主内容区 -->
      <n-layout>
        <n-layout-content content-style="height: 100vh; display: flex; flex-direction: column;">
          <!-- 消息区域 -->
          <div class="messages-container">
            <n-card
              v-for="(message, index) in messagesList"
              :key="index"
              :title="message.role === 'user' ? '你' : 'DeepSeek'"
              style="margin: 12px;"
              :bordered="false"
              size="small"
            >
              {{ message.content }}
            </n-card>
          </div>

          <!-- 输入区域 -->
          <div class="input-area">
            <n-input-group style="padding: 16px; background: #fff; border-top: 1px solid #eee;">
              <n-input 
                round
                placeholder="输入消息..."
                type="textarea"
                :autosize="{maxRows: 5}"
                v-model="currentUserMessage"
                @keyup.enter="sendUserMessage"
                style="flex: 1;"
              />
              <n-button 
                round
                type="primary"
                @click="sendUserMessage"
                style="margin-left: 12px;"
              >
                <template #icon>
                  <n-icon><Send /></n-icon>
                </template>
                发送
              </n-button>
            </n-input-group>
          </div>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { 
  NLayout, 
  NLayoutSider, 
  NLayoutContent,
  NButton,
  NIcon,
  NCard,
  NInput,
  NInputGroup,
  NScrollbar
} from 'naive-ui'
import { 
  Add, 
  Send, 
  ChatbubbleEllipses,
  Settings, 
  Close 
} from '@vicons/ionicons5'

// 消息类型
interface ChatMessage {
  role: string
  content: string
}

// 历史记录类型
interface ChatHistory {
  id: string
  title: string
  messages: ChatMessage[]
}

// 数据
const currentUserMessage = ref('')
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
    role: 'assistant', 
    content: '我是DeepSeek，请问有什么可以帮助您？' 
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

// 发送消息
const sendUserMessage = () => {
  if (!currentUserMessage.value.trim()) return

  const userMessage = currentUserMessage.value
  currentUserMessage.value = ''

  messagesList.push(
    { role: 'user', content: userMessage },
    { role: 'assistant', content: '正在思考...' }
  )

  // 更新当前对话历史
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

  // 模拟AI回复
  setTimeout(() => {
    messagesList[messagesList.length - 1].content = 
      `这是对"${userMessage}"的模拟回复。实际使用时请接入AI API。`
  }, 1000)
}
</script>

<style scoped>
.full-container {
  height: 100%;
  padding-bottom: 30px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  background: #fafafa;
}

.input-area {
  position: relative;
  bottom: 0;
  background: #fff;
}

/* 历史记录项样式 */
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
</style>