<template>
  <div class="chat-page">
    <div class="chat-sidebar">
      <h3>💬 AI营养师对话</h3>

      <el-button
        type="primary"
        style="width: 100%;"
        @click="handleAnalyze"
      >
        <el-icon>
          <DataAnalysis />
        </el-icon>
        AI健康分析
      </el-button>

      <div class="quick-questions">
        <h4>常见问题</h4>

        <div
          v-for="q in quickQuestions"
          :key="q"
          class="quick-question-item"
          @click="sendQuickQuestion(q)"
        >
          {{ q }}
        </div>
      </div>
    </div>

    <div class="chat-main">
      <div class="chat-messages" ref="messagesRef">
        <div
          v-if="messages.length === 0"
          class="welcome-message"
        >
          <h2>你好！我是你的AI营养师 🥗</h2>
          <p>我可以根据你的体检报告和口味偏好，提供个性化的营养建议。</p>
        </div>

        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['chat-bubble', msg.role]"
        >
          <div
            class="bubble-content"
            v-html="formatMessage(msg.content)"
          />
        </div>

        <div
          v-if="thinking"
          class="chat-bubble assistant"
        >
          <div class="thinking">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="输入您的问题，例如：高血压患者应该吃什么？"
          @keydown.enter.exact="handleSend"
          :disabled="thinking"
        />

        <el-button
          type="primary"
          :loading="thinking"
          @click="handleSend"
          style="margin-top: 8px;"
        >
          <el-icon>
            <Promotion />
          </el-icon>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { agentChat, analyzeHealth } from '@/api'
import { useUserStore } from '@/stores/user'
import {
  DataAnalysis,
  Promotion
} from '@element-plus/icons-vue'
import { marked } from 'marked'

const userStore = useUserStore()

const messages = ref<any[]>([])
const inputMessage = ref('')
const thinking = ref(false)
const messagesRef = ref()

const quickQuestions = [
  '高血压患者应该吃什么？',
  '糖尿病饮食注意事项',
  '减肥期间怎么吃？',
  '高尿酸患者能吃什么？'
]

async function handleSend() {
  if (!inputMessage.value.trim() || thinking.value) {
    return
  }

  const userMsg = inputMessage.value.trim()

  messages.value.push({
    role: 'user',
    content: userMsg
  })

  inputMessage.value = ''
  thinking.value = true

  scrollToBottom()

  try {
    const res = await agentChat(
      userStore.userId,
      userMsg
    )

    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.response
      })
    }
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，服务暂时不可用，请稍后再试。'
    })
  }

  thinking.value = false
  scrollToBottom()
}

async function handleAnalyze() {
  thinking.value = true

  try {
    const res = await analyzeHealth(userStore.userId)

    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.analysis
      })
    }
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '健康分析失败，请稍后再试。'
    })
  }

  thinking.value = false
  scrollToBottom()
}

function sendQuickQuestion(q: string) {
  inputMessage.value = q
  handleSend()
}

function formatMessage(content: string) {
  return marked(content)
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop =
        messagesRef.value.scrollHeight
    }
  })
}
</script>