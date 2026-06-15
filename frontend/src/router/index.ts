import { createRouter, createWebHistory } from 'vue-router'

import Chat from '@/views/Chat.vue'
import Dashboard from '@/views/Dashboard.vue'
import Health from '@/views/Health.vue'
import MealPlan from '@/views/MealPlan.vue'
import Preferences from '@/views/Preferences.vue'


const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      component: Dashboard
    },
    {
      path: '/health',
      component: Health
    },
    {
      path: '/preferences',
      component: Preferences
    },
    {
      path: '/meal-plan',
      component: MealPlan
    },
    {
      path: '/chat',
      component: Chat
    }
  ]
})

export default router