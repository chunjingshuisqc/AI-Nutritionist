import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 用户管理
export async function createUser(data: any) {
  return (await api.post('/users/', data)).data
}

export async function getUser(userId: number) {
  return (await api.get(`/users/${userId}`)).data
}

// 体检报告
export async function createHealthReport(
  userId: number,
  data: any
) {
  return (await api.post(`/health/${userId}`, data)).data
}

export async function getHealthReports(userId: number) {
  return (await api.get(`/health/${userId}/reports`)).data
}

// 口味偏好
export async function savePreferences(
  userId: number,
  data: any
) {
  return (await api.post(`/preferences/${userId}`, data)).data
}

export async function getPreferences(userId: number) {
  return (await api.get(`/preferences/${userId}`)).data
}

// 食谱管理
export async function generateMealPlan(
  userId: number,
  planName?: string
) {
  return (
    await api.post(
      `/meal-plans/generate/${userId}`,
      {
        plan_name: planName || '智能周食谱'
      }
    )
  ).data
}

export async function listMealPlans(userId: number) {
  return (await api.get(`/meal-plans/${userId}`)).data
}

export async function getMealPlanDetail(planId: number) {
  return (await api.get(`/meal-plans/detail/${planId}`)).data
}

// AI Agent对话
export async function agentChat(
  userId: number,
  message: string,
  context?: any
) {
  return (
    await api.post(
      `/agent/chat/${userId}`,
      {
        message,
        context
      }
    )
  ).data
}

export async function analyzeHealth(userId: number) {
  return (await api.post(`/agent/analyze/${userId}`)).data
}

export default api