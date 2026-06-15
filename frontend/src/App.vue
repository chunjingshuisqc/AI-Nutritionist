<template>
  <div id="app-root">
    <el-header class="app-header" v-if="userStore.isLoggedIn">
      <div class="header-content">
        <div class="logo" @click="router.push('/')">
          <el-icon :size="28">
            <Food />
          </el-icon>
          <span class="logo-text">AI营养师</span>
        </div>

        <div class="nav-menu">
          <el-menu
            :default-active="route.path"
            mode="horizontal"
            router
          >
            <el-menu-item index="/dashboard">
              <el-icon>
                <DataAnalysis />
              </el-icon>
              <span>控制台</span>
            </el-menu-item>

            <el-menu-item index="/health">
              <el-icon>
                <FirstAidKit />
              </el-icon>
              <span>体检报告</span>
            </el-menu-item>

            <el-menu-item index="/preferences">
              <el-icon>
                <Setting />
              </el-icon>
              <span>口味偏好</span>
            </el-menu-item>

            <el-menu-item index="/meal-plan">
              <el-icon>
                <Bowl />
              </el-icon>
              <span>智能食谱</span>
            </el-menu-item>

            <el-menu-item index="/chat">
              <el-icon>
                <ChatDotRound />
              </el-icon>
              <span>AI咨询</span>
            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </el-header>

    <el-main class="app-main">
      <router-view />
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  Food,
  DataAnalysis,
  FirstAidKit,
  Setting,
  Bowl,
  ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

onMounted(() => {
  userStore.init()
})
</script>