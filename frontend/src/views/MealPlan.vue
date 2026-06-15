<template>
  <el-card>
    <h2>智能周食谱</h2>

    <el-button
      type="primary"
      :loading="loading"
      @click="generate"
    >
      生成模拟周食谱
    </el-button>

    <div v-if="plan" style="margin-top: 20px;">
      <h3>{{ plan.title }}</h3>

      <el-card
        v-for="day in plan.days"
        :key="day.day"
        style="margin-bottom: 12px;"
      >
        <h4>{{ day.day }}</h4>
        <p>早餐：{{ day.breakfast }}</p>
        <p>午餐：{{ day.lunch }}</p>
        <p>晚餐：{{ day.dinner }}</p>
      </el-card>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

import { generateMealPlan } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const loading = ref(false)
const plan = ref<any>(null)

async function generate() {
  if (!userStore.userId) {
    ElMessage.warning('请先加载模拟用户')
    return
  }

  loading.value = true

  try {
    const res = await generateMealPlan(
      userStore.userId,
      '模拟健康周食谱'
    )

    if (res.code === 200) {
      plan.value = res.data
      ElMessage.success('食谱生成成功')
    }
  } catch (error) {
    ElMessage.error('食谱生成失败')
  } finally {
    loading.value = false
  }
}
</script>