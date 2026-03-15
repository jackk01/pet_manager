<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="250px" class="sidebar">
      <div class="logo">
        <el-icon size="32" color="#409eff">
          <House />
        </el-icon>
        <span class="title">宠物管理系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/pets">
          <el-icon><House /></el-icon>
          <span>宠物管理</span>
        </el-menu-item>
        <el-menu-item index="/vaccinations">
          <el-icon><Tools /></el-icon>
          <span>疫苗管理</span>
        </el-menu-item>
        <el-menu-item index="/health">
          <el-icon><FirstAidKit /></el-icon>
          <span>健康管理</span>
        </el-menu-item>
        <el-menu-item index="/expenses">
          <el-icon><Money /></el-icon>
          <span>消费管理</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据统计</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区域 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left"></div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" :src="userInfo?.avatar" icon="User" />
              <span class="username">{{ userInfo?.nickname || userInfo?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getUserInfo } from '@/api/auth'
import {
  House,
  Odometer,
  Tools,
  FirstAidKit,
  Money,
  DataAnalysis,
  User,
  ArrowDown
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const userInfo = ref(userStore.userInfo)

onMounted(() => {
  if (!userInfo.value) {
    fetchUserInfo()
  }
})

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const res = await getUserInfo()
    userStore.setUserInfo(res)
    userInfo.value = res
  } catch (e) {
    console.error('获取用户信息失败:', e)
    userStore.logout()
    router.push('/login')
  }
}

// 下拉菜单命令处理
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    userStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  }).catch(() => {
    // 取消操作
  })
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background-color: #304156;
  overflow: hidden;

  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    padding: 20px 0;
    color: #fff;
    background-color: #263445;

    .title {
      margin-left: 10px;
      font-size: 18px;
      font-weight: bold;
    }
  }

  :deep(.el-menu) {
    border-right: none;
  }
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100vh;

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    background-color: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, .08);

    .header-right {
      .user-info {
        display: flex;
        align-items: center;
        cursor: pointer;

        .username {
          margin: 0 8px;
          font-size: 14px;
        }
      }
    }
  }

  .content {
    flex: 1;
    overflow-y: auto;
    background-color: #f5f7fa;
    padding: 20px;
  }
}

// 页面切换动画
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
