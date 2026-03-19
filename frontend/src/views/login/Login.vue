<template>
  <div class="login-container">
    <div class="bg-layer bg-gradient"></div>
    <div class="bg-layer bg-orbs"></div>
    <div
      ref="pawLayerRef"
      class="bg-layer bg-paws"
      @click="triggerPawGrip"
      @mousemove="handlePawMove"
      @mouseleave="releasePaws"
    >
      <span
        v-for="paw in paws"
        :key="paw.id"
        class="paw"
        :class="{ grip: grippingPawIds.includes(paw.id), lift: liftedPawIds.includes(paw.id) }"
        :style="{
          '--x': paw.left,
          '--y': paw.top,
          '--size': `${paw.size}px`,
          '--r': `${paw.rotate}deg`,
          '--delay': `${paw.delay}s`,
          '--opa': paw.opacity
        }"
      >
        <span class="paw-shape"></span>
      </span>
    </div>
    <div class="bg-layer bg-grid"></div>
    <div class="login-box">
      <div class="login-header">
        <h2>宠物信息管理系统</h2>
        <p>欢迎使用，请登录您的账号</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-links">
          <span @click="switchToRegister">还没有账号？立即注册</span>
        </div>
      </el-form>
    </div>
    
    <!-- 注册弹窗 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="用户注册"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="registerLoading" @click="handleRegister">
          注册
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { login, register } from '@/api/auth'
import type { LoginDto, RegisterDto } from '@/types/user'

const router = useRouter()
const userStore = useUserStore()

interface PawItem {
  id: number
  left: string
  top: string
  size: number
  rotate: number
  delay: number
  opacity: number
}

const paws = ref<PawItem[]>([
  { id: 1, left: '8%', top: '10%', size: 72, rotate: -12, delay: -1.2, opacity: 0.14 },
  { id: 2, left: '76%', top: '22%', size: 88, rotate: 14, delay: -3.6, opacity: 0.13 },
  { id: 3, left: '12%', top: '58%', size: 96, rotate: -7, delay: -5.2, opacity: 0.16 },
  { id: 4, left: '71%', top: '68%', size: 74, rotate: 10, delay: -0.6, opacity: 0.12 },
  { id: 5, left: '32%', top: '40%', size: 66, rotate: 18, delay: -4.3, opacity: 0.11 },
  { id: 6, left: '47%', top: '14%', size: 78, rotate: -16, delay: -2.1, opacity: 0.13 },
  { id: 7, left: '38%', top: '78%', size: 86, rotate: 8, delay: -6.7, opacity: 0.12 },
  { id: 8, left: '62%', top: '33%', size: 70, rotate: -9, delay: -7.9, opacity: 0.14 },
  { id: 9, left: '20%', top: '28%', size: 64, rotate: 11, delay: -2.8, opacity: 0.11 },
  { id: 10, left: '84%', top: '52%', size: 82, rotate: -14, delay: -4.9, opacity: 0.13 },
  { id: 11, left: '55%', top: '74%', size: 68, rotate: 7, delay: -1.7, opacity: 0.12 },
  { id: 12, left: '26%', top: '66%', size: 76, rotate: -5, delay: -6.1, opacity: 0.12 }
])
const grippingPawIds = ref<number[]>([])
const liftedPawIds = ref<number[]>([])
const pawLayerRef = ref<HTMLElement>()

// 登录表单
const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const loginForm = reactive<LoginDto>({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度在 6 到 32 个字符', trigger: 'blur' }
  ]
}

// 注册表单
const registerDialogVisible = ref(false)
const registerFormRef = ref<FormInstance>()
const registerLoading = ref(false)
const registerForm = reactive<RegisterDto & { confirmPassword: string }>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度在 6 到 32 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const res = await login(loginForm)
        userStore.setToken(res.access_token)
        await userStore.getUserInfo()
        ElMessage.success('登录成功')
        router.push('/dashboard')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    }
  })
}

// 切换到注册
const switchToRegister = () => {
  registerDialogVisible.value = true
  registerForm.username = ''
  registerForm.email = ''
  registerForm.password = ''
  registerForm.confirmPassword = ''
  if (registerFormRef.value) {
    registerFormRef.value.resetFields()
  }
}

// 注册处理
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      registerLoading.value = true
      try {
        const { confirmPassword, ...registerData } = registerForm
        await register(registerData)
        ElMessage.success('注册成功，请登录')
        registerDialogVisible.value = false
        loginForm.username = registerData.username
        loginForm.password = registerData.password
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '注册失败，请稍后重试')
      } finally {
        registerLoading.value = false
      }
    }
  })
}

const triggerPawGrip = () => {
  const source = [...paws.value]
  if (source.length === 0) return
  source.sort(() => Math.random() - 0.5)
  const count = Math.min(source.length, Math.floor(Math.random() * 3) + 3)
  grippingPawIds.value = source.slice(0, count).map((item) => item.id)
}

const releasePaws = () => {
  grippingPawIds.value = []
  liftedPawIds.value = []
}

const handlePawMove = (event: MouseEvent) => {
  if (!pawLayerRef.value) return
  const rect = pawLayerRef.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top

  const nearby = paws.value
    .map((paw) => {
      const leftPercent = Number.parseFloat(paw.left) / 100
      const topPercent = Number.parseFloat(paw.top) / 100
      const centerX = rect.width * leftPercent + paw.size / 2
      const centerY = rect.height * topPercent + paw.size / 2
      const distance = Math.hypot(mouseX - centerX, mouseY - centerY)
      return { id: paw.id, distance }
    })
    .filter((item) => item.distance <= 150)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 4)
    .map((item) => item.id)

  liftedPawIds.value = nearby
}
</script>

<style scoped>
.login-container {
  position: relative;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
  background: #101a34;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bg-layer {
  position: absolute;
  inset: -10%;
  pointer-events: none;
}

.bg-gradient {
  z-index: 0;
  background:
    radial-gradient(circle at 15% 20%, rgba(79, 172, 254, 0.35) 0%, rgba(79, 172, 254, 0) 40%),
    radial-gradient(circle at 85% 18%, rgba(161, 140, 209, 0.35) 0%, rgba(161, 140, 209, 0) 42%),
    radial-gradient(circle at 70% 80%, rgba(255, 164, 141, 0.24) 0%, rgba(255, 164, 141, 0) 45%),
    linear-gradient(140deg, #0d1730 0%, #15254a 45%, #10203e 100%);
}

.bg-orbs::before,
.bg-orbs::after {
  content: '';
  position: absolute;
  width: 38vmax;
  height: 38vmax;
  border-radius: 50%;
  filter: blur(12px);
  opacity: 0.42;
}

.bg-orbs::before {
  top: -8vmax;
  left: -6vmax;
  background: radial-gradient(circle, rgba(91, 216, 255, 0.7) 0%, rgba(91, 216, 255, 0) 70%);
  animation: floatA 16s ease-in-out infinite;
}

.bg-orbs::after {
  right: -10vmax;
  bottom: -10vmax;
  background: radial-gradient(circle, rgba(190, 139, 255, 0.65) 0%, rgba(190, 139, 255, 0) 72%);
  animation: floatB 18s ease-in-out infinite;
}

.bg-orbs {
  z-index: 1;
}

.bg-grid {
  z-index: 2;
  opacity: 0.16;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 34px 34px;
  animation: drift 28s linear infinite;
}

.bg-paws {
  z-index: 3;
  overflow: hidden;
  pointer-events: auto;
}

.paw {
  display: block;
  position: absolute;
  left: var(--x);
  top: var(--y);
  width: var(--size);
  height: var(--size);
  --r: 0deg;
  opacity: var(--opa);
  transform-origin: center;
  animation: pawFloat 9s ease-in-out infinite;
  animation-delay: var(--delay);
}

.paw-shape {
  display: block;
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 160'%3E%3Cg fill='%23ffffff'%3E%3Cellipse cx='44' cy='54' rx='11' ry='15'/%3E%3Cellipse cx='66' cy='43' rx='11' ry='15'/%3E%3Cellipse cx='92' cy='43' rx='11' ry='15'/%3E%3Cellipse cx='114' cy='54' rx='11' ry='15'/%3E%3Cpath d='M80 67c-22 0-39 15-39 35 0 15 13 24 39 24s39-9 39-24c0-20-17-35-39-35z'/%3E%3C/g%3E%3C/svg%3E");
  transition: transform 0.2s ease, filter 0.2s ease, opacity 0.2s ease;
  opacity: 0.95;
  filter: drop-shadow(0 2px 6px rgba(8, 23, 52, 0.14));
}

.paw.lift .paw-shape {
  transform: translateY(-3px) scale(1.02);
  filter: brightness(1.08);
}

.paw.grip .paw-shape {
  animation: pawGrip 0.35s ease;
  transform: scale(0.92);
  filter: brightness(1.15);
}

.bg-paws:active .paw-shape {
  transition-duration: 0.14s;
}

.login-box {
  position: relative;
  z-index: 20;
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(4px);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 12, 40, 0.35);
  animation: boxUp 0.6s ease;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #333;
  font-size: 28px;
  margin-bottom: 8px;
  font-weight: 600;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  font-weight: 500;
}

.login-links {
  text-align: center;
}

.login-links span {
  color: #409eff;
  cursor: pointer;
  font-size: 14px;
}

.login-links span:hover {
  text-decoration: underline;
}

@keyframes floatA {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(2.5vmax, 2vmax); }
}

@keyframes floatB {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-2.5vmax, -2vmax); }
}

@keyframes drift {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-34px, -34px); }
}

@keyframes pawFloat {
  0%, 100% { transform: translate3d(0, 0, 0) rotate(var(--r)) scale(1); }
  35% { transform: translate3d(6px, -8px, 0) rotate(var(--r)) scale(1.03); }
  70% { transform: translate3d(-5px, 4px, 0) rotate(var(--r)) scale(0.98); }
}

@keyframes pawGrip {
  0% { transform: scale(1); }
  50% { transform: scale(0.85) translateY(1px); }
  100% { transform: scale(0.92); }
}

@keyframes boxUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
