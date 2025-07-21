<template>
<n-flex vertical>
    <div class="message-view">
    <n-flex vertical>
        <n-scrollbar ref="scrollbarRef" style="height: 80vh; overflow-y: auto;">
        <n-card
        v-for="(message) in messagesList"
        :key="nanoid()"
        :title="message.role"
        >
        {{ message.content }}
        </n-card>
        </n-scrollbar>
    </n-flex>
    </div>
    <n-input-group class="chat-message-send">
        <n-input round placeholder = "请输入您的问题"
            type="textarea"
            :autosize="{maxRows: 5}"
            v-model:value="currentUserMessage"
            @keyup.enter="sendUserMessage" 
            class="chat-message-send-input"
        />
        <n-button ghost round
            type="primary"
            @click="sendUserMessage"
            class="chat-message-send-button"
            >Send</n-button>  
    </n-input-group>

</n-flex>    
</template>

<script lang="ts"> export default {name:"Chat"}</script>
<script setup lang="ts">
import {NCard, NInputGroup ,NFlex, NButton, NInput, NScrollbar} from 'naive-ui'
import {ref, reactive, nextTick} from 'vue'
import {nanoid} from 'nanoid'
import {type ChatMessage} from '@/types'
import {sendMessageToOpenAI, getContentFromOpenAIResponse} from '@/hooks/chat-with-openai'

let currentUserMessage = ref("")
let scrollbarRef = ref()
let messagesList: Array<ChatMessage> = reactive([
    {
        role: "agent",
        content: "Hello! How can I assist you today?"
    }
]) 

// 滚动到底部的函数
function scrollToBottom() {
    nextTick(() => {
        if (scrollbarRef.value) {
            scrollbarRef.value.scrollTo({
                top: -100,
                behavior: 'smooth'
            });
        }
    });
} 

async function sendUserMessage() {
    console.log("sendUserMessage", currentUserMessage.value);
    if (currentUserMessage.value) {
        let sendMessage = currentUserMessage.value
        currentUserMessage.value = "";
        messagesList.push({
            role: "user",
            content: sendMessage
        });
        scrollToBottom(); // 添加用户消息后滚动到底部
        
        messagesList.push({
            role: "agent",
            content: "正在思考中..."
        });
        scrollToBottom(); // 添加思考消息后滚动到底部
        
        let agentResponse = await sendMessageToOpenAI(sendMessage);
        if (agentResponse) {
            await getContentFromOpenAIResponse(agentResponse, messagesList)
            scrollToBottom(); // 获取到回复后滚动到底部
        }
        else {
            messagesList[messagesList.length - 1].content = "请求失败，请稍后再试";  
            scrollToBottom(); // 显示错误消息后滚动到底部
        }
    }
}

</script>

<style scope>
.message-view {
    margin-left: 5%;
}
.chat-message-send {
    left: 0;
    bottom: 0;
    margin-bottom: 5%;
    margin-left: 5%;
    margin-right: 5%;
    width: 90%;
}
.chat-message-send-input {
    width:50%;
    margin-right: 10px;
}
.chat-message-send-button {
    margin-left: 10px;
}
</style>