<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '88px' : '240px'" class="sidebar" :class="{ collapsed: isCollapse }">
      <div class="logo">
        <div class="brand-icon">
          <el-icon :size="isCollapse ? 20 : 22">
            <House />
          </el-icon>
        </div>
        <transition name="brand-fade">
          <div v-if="!isCollapse" class="brand-text">
            <p class="title">宠物管家</p>
            <p class="subtitle">Pet Care Center</p>
          </div>
        </transition>
      </div>
      <el-menu
        :default-active="$route.path"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        background-color="transparent"
        text-color="#e8edf8"
        active-text-color="#ffe7cf"
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
        <div class="header-left">
          <el-button class="collapse-btn" text @click="toggleSidebar">
            <el-icon size="18">
              <component :is="isCollapse ? Expand : Fold" />
            </el-icon>
          </el-button>
        </div>
        <div class="header-right">
          <el-badge :value="unreadNoticeCount > 99 ? '99+' : unreadNoticeCount" :hidden="unreadNoticeCount === 0">
            <el-button class="notice-btn" text @click="openNoticeDialog">
              <el-icon size="17"><Bell /></el-icon>
            </el-button>
          </el-badge>
          <div class="theme-switch-wrap" :class="{ dark: isDarkTheme }">
            <el-icon class="theme-switch-icon">
              <Sunny />
            </el-icon>
            <el-switch
              v-model="isDarkTheme"
              class="compact-theme-switch"
              @change="toggleColorTheme"
            />
            <el-icon class="theme-switch-icon">
              <MoonNight />
            </el-icon>
          </div>
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

      <el-dialog
        v-model="noticeDialogVisible"
        title="站内信提醒"
        width="560px"
        :close-on-click-modal="false"
      >
        <div class="notice-toolbar">
          <el-switch
            v-model="onlyUnreadNotice"
            inline-prompt
            active-text="仅未读"
            inactive-text="全部"
            @change="refreshNoticeList"
          />
          <el-button text @click="markAllNoticeRead" :disabled="unreadNoticeCount === 0">
            全部标记已读
          </el-button>
        </div>
        <div v-loading="noticeLoading" class="notice-list">
          <div v-if="noticeList.length === 0" class="notice-empty">
            <el-empty description="暂无提醒消息" />
          </div>
          <div
            v-for="item in noticeList"
            :key="item.id"
            class="notice-item"
            :class="{ unread: !item.is_read }"
          >
            <div class="notice-head">
              <div class="notice-title">
                <el-tag size="small" :type="item.message_type === 'vaccination' ? 'warning' : 'success'">
                  {{ item.message_type_display }}
                </el-tag>
                <span>{{ item.title }}</span>
              </div>
              <el-button text size="small" @click="markNoticeRead(item)" :disabled="item.is_read">
                {{ item.is_read ? '已读' : '标记已读' }}
              </el-button>
            </div>
            <p class="notice-content">{{ item.content }}</p>
            <div class="notice-meta">
              <span v-if="item.due_date">到期日：{{ item.due_date }}</span>
              <span v-if="item.days_left !== null && item.days_left !== undefined">
                {{ item.days_left < 0 ? `逾期${Math.abs(item.days_left)}天` : item.days_left === 0 ? '今天到期' : `${item.days_left}天后到期` }}
              </span>
            </div>
          </div>
        </div>
        <div class="notice-pagination">
          <el-pagination
            v-model:current-page="noticePagination.page"
            v-model:page-size="noticePagination.size"
            :total="noticePagination.total"
            :page-sizes="[5, 10, 20]"
            layout="total, sizes, prev, pager, next"
            @size-change="refreshNoticeList"
            @current-change="refreshNoticeList"
          />
        </div>
      </el-dialog>

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
import { ref, onMounted, onUnmounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getUserInfo } from '@/api/auth'
import { getNotifications, getNotificationUnreadCount, markNotificationsRead } from '@/api/notification'
import type { NotificationDto } from '@/types/notification'
import {
  House,
  Odometer,
  Tools,
  FirstAidKit,
  Money,
  DataAnalysis,
  User,
  ArrowDown,
  Fold,
  Expand,
  Sunny,
  MoonNight,
  Bell
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const userInfo = ref(userStore.userInfo)
const isCollapse = ref(false)
const isDarkTheme = ref(false)
const unreadNoticeCount = ref(0)
const noticeDialogVisible = ref(false)
const onlyUnreadNotice = ref(false)
const noticeLoading = ref(false)
const noticeList = ref<NotificationDto[]>([])
const noticePagination = reactive({
  page: 1,
  size: 10,
  total: 0,
})
let noticePollingTimer: number | null = null

onMounted(() => {
  applySavedColorTheme()
  fetchUnreadNoticeCount()
  noticePollingTimer = window.setInterval(() => {
    fetchUnreadNoticeCount()
  }, 60000)
  if (!userInfo.value) {
    fetchUserInfo()
  }
})

onUnmounted(() => {
  if (noticePollingTimer) {
    window.clearInterval(noticePollingTimer)
    noticePollingTimer = null
  }
})

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const res = await getUserInfo() as any
    userStore.setUserInfo(res as any)
    userInfo.value = res as any
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

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const applyColorTheme = (darkMode: boolean) => {
  if (darkMode) {
    document.documentElement.setAttribute('data-theme', 'dark')
  } else {
    document.documentElement.removeAttribute('data-theme')
  }
}

const applySavedColorTheme = () => {
  const savedTheme = localStorage.getItem('ui_theme')
  isDarkTheme.value = savedTheme === 'dark'
  applyColorTheme(isDarkTheme.value)
}

const toggleColorTheme = () => {
  localStorage.setItem('ui_theme', isDarkTheme.value ? 'dark' : 'light')
  applyColorTheme(isDarkTheme.value)
}

const fetchUnreadNoticeCount = async () => {
  try {
    const res = await getNotificationUnreadCount(14)
    unreadNoticeCount.value = Number((res as any)?.unread_count || 0)
  } catch (e) {
    console.error('获取未读站内信失败:', e)
  }
}

const refreshNoticeList = async () => {
  noticeLoading.value = true
  try {
    const res = await getNotifications({
      page: noticePagination.page,
      size: noticePagination.size,
      unread_only: onlyUnreadNotice.value,
      days: 14,
    })
    noticeList.value = ((res as any)?.items || []) as NotificationDto[]
    noticePagination.total = Number((res as any)?.total || 0)
    unreadNoticeCount.value = Number((res as any)?.unread_count || 0)
  } catch (e) {
    ElMessage.error('加载站内信失败，请稍后重试')
  } finally {
    noticeLoading.value = false
  }
}

const openNoticeDialog = async () => {
  noticeDialogVisible.value = true
  noticePagination.page = 1
  await refreshNoticeList()
}

const markNoticeRead = async (item: NotificationDto) => {
  if (item.is_read) return
  try {
    const res = await markNotificationsRead({ ids: [item.id] })
    item.is_read = true
    unreadNoticeCount.value = Number((res as any)?.unread_count || 0)
  } catch (e) {
    ElMessage.error('更新消息状态失败')
  }
}

const markAllNoticeRead = async () => {
  try {
    await markNotificationsRead({ read_all: true })
    noticeList.value = noticeList.value.map((item) => ({ ...item, is_read: true }))
    unreadNoticeCount.value = 0
    ElMessage.success('已全部标记为已读')
  } catch (e) {
    ElMessage.error('操作失败，请稍后重试')
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
  background: linear-gradient(180deg, #1d2b45 0%, #283c63 55%, #314a78 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  transition: width 0.25s ease;
  overflow: hidden;

  .logo {
    display: flex;
    align-items: center;
    height: 72px;
    padding: 0 18px;
    color: #fff;
    background: rgba(13, 23, 42, 0.26);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);

    .brand-icon {
      width: 38px;
      height: 38px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #183149;
      background: linear-gradient(145deg, #ffd9b3 0%, #ffb287 100%);
      box-shadow: 0 8px 14px rgba(255, 178, 135, 0.38);
      flex-shrink: 0;
    }

    .brand-text {
      margin-left: 10px;
      min-width: 0;

      .title {
        margin: 0;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.3px;
      }

      .subtitle {
        margin: 2px 0 0;
        font-size: 11px;
        color: rgba(232, 237, 248, 0.7);
      }
    }
  }

  :deep(.el-menu) {
    border-right: none;
    padding: 12px 8px;
  }

  :deep(.el-menu-item) {
    height: 46px;
    border-radius: 10px;
    margin-bottom: 6px;
    color: #e8edf8;
    transition: all 0.2s ease;
  }

  :deep(.el-menu-item:hover) {
    background: rgba(255, 255, 255, 0.14);
  }

  :deep(.el-menu-item.is-active) {
    background: linear-gradient(135deg, rgba(255, 195, 141, 0.28), rgba(255, 162, 124, 0.34));
    box-shadow: inset 0 0 0 1px rgba(255, 223, 190, 0.35);
    color: #fff2e4 !important;
  }
}

.sidebar.collapsed {
  .logo {
    padding: 0 0;
    justify-content: center;
  }

  :deep(.el-menu--collapse) {
    width: 100%;
  }

  :deep(.el-menu--collapse .el-menu-item) {
    justify-content: center;
    padding: 0 !important;
  }

  :deep(.el-menu--collapse .el-menu-item .el-icon) {
    margin-right: 0 !important;
    margin-left: 0 !important;
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
    padding: 0 16px;
    background: rgba(255, 255, 255, 0.62);
    background: var(--topbar-bg);
    border-bottom: 1px solid var(--topbar-border);
    backdrop-filter: var(--topbar-blur);
    -webkit-backdrop-filter: var(--topbar-blur);
    box-shadow: var(--topbar-shadow);

    .header-left {
      display: flex;
      align-items: center;
    }

    .collapse-btn {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      color: var(--text-secondary);
    }

    .collapse-btn:hover {
      background: var(--input-bg);
      color: var(--text-primary);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;

      .notice-btn {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        color: var(--text-secondary);
        border: 1px solid var(--section-border);
        background: var(--input-bg);
      }

      .notice-btn:hover {
        background: var(--acrylic-bg-strong);
        color: var(--text-primary);
      }

      .theme-switch-wrap {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        height: 30px;
        padding: 0 8px;
        border-radius: 999px;
        border: 1px solid var(--section-border);
        background: var(--input-bg);
        transition: all 0.2s ease;
      }

      .theme-switch-wrap.dark {
        box-shadow: inset 0 0 0 1px rgba(120, 162, 223, 0.3);
      }

      .theme-switch-icon {
        color: var(--text-secondary);
        font-size: 13px;
        opacity: 0.8;
      }

      :deep(.compact-theme-switch .el-switch__core) {
        width: 34px !important;
        height: 18px;
        border-radius: 99px;
        border-color: rgba(122, 153, 204, 0.28);
        background: rgba(211, 224, 248, 0.9);
      }

      :deep(.compact-theme-switch.is-checked .el-switch__core) {
        background: rgba(85, 121, 181, 0.9);
        border-color: rgba(108, 153, 225, 0.65);
      }

      :deep(.compact-theme-switch .el-switch__action) {
        width: 14px;
        height: 14px;
      }

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
    background: transparent;
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

.brand-fade-enter-active,
.brand-fade-leave-active {
  transition: all 0.2s ease;
}

.brand-fade-enter-from,
.brand-fade-leave-to {
  opacity: 0;
  transform: translateX(-6px);
}

.notice-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.notice-list {
  min-height: 220px;
  max-height: 420px;
  overflow-y: auto;
  padding-right: 4px;
}

.notice-empty {
  padding: 18px 0;
}

.notice-item {
  border: 1px solid var(--section-border);
  background: var(--acrylic-bg);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 10px;
}

.notice-item.unread {
  border-color: rgba(64, 158, 255, 0.34);
  box-shadow: 0 8px 18px rgba(64, 158, 255, 0.12);
}

.notice-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.notice-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-primary);
}

.notice-content {
  margin: 8px 0 6px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.notice-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 12px;
}

.notice-pagination {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}

</style>
