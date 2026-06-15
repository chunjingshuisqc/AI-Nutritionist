import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import * as api from '@/api'


export const useUserStore = defineStore('user', () => {
  const currentUser = ref<any>(null)
  const preferences = ref<any>(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => currentUser.value !== null)
  const userId = computed(() => currentUser.value?.id || 0)
  const bmi = computed(() => currentUser.value?.bmi || 0)

  function init() {
  const savedUserId = localStorage.getItem(
    'nutritionist_user_id'
  )

  if (savedUserId) {
    fetchUser(Number(savedUserId))
  } else {
    // 开发测试阶段默认加载ID为1的用户
    fetchUser(1)
  }
}

  async function fetchUser(uid: number) {
    loading.value = true

    try {
      const res = await api.getUser(uid)

      if (res.code === 200) {
        currentUser.value = res.data

        localStorage.setItem(
          'nutritionist_user_id',
          String(uid)
        )

        fetchPreferences(uid)
      }
    } finally {
      loading.value = false
    }
  }

  async function createUser(data: any) {
    loading.value = true

    try {
      const res = await api.createUser(data)

      if (res.code === 200) {
        currentUser.value = res.data

        localStorage.setItem(
          'nutritionist_user_id',
          String(res.data.id)
        )

        return res.data
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchPreferences(uid: number) {
    const res = await api.getPreferences(uid)

    if (res.code === 200) {
      preferences.value = res.data
    }
  }

  async function savePreferences(data: any) {
    const res = await api.savePreferences(
      currentUser.value.id,
      data
    )

    if (res.code === 200) {
      preferences.value = res.data
    }
  }

  function logout() {
    currentUser.value = null
    preferences.value = null

    localStorage.removeItem('nutritionist_user_id')
  }

  return {
    currentUser,
    preferences,
    loading,
    isLoggedIn,
    userId,
    bmi,
    init,
    fetchUser,
    createUser,
    savePreferences,
    logout
  }
})