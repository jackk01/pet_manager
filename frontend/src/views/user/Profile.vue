<template>
  <div class="profile-container">
    <div class="page-header">
      <h2>个人中心</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="avatar-card">
          <div class="avatar-content">
            <div class="avatar-wrapper">
              <el-avatar :size="120" :src="userInfo.avatar || defaultAvatar">
                {{ userInfo.username?.charAt(0) }}
              </el-avatar>
              <el-button
                class="upload-btn"
                type="primary"
                size="small"
                @click="avatarUploadRef?.click()"
              >
                更换头像
              </el-button>
              <input
                ref="avatarUploadRef"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleAvatarUpload"
              />
            </div>
            <div class="user-basic">
              <h3>{{ userInfo.username }}</h3>
              <p class="user-email">{{ userInfo.email }}</p>
              <el-tag type="success" size="small">已激活</el-tag>
            </div>
          </div>
        </el-card>

        <el-card class="stats-card" style="margin-top: 20px">
          <template #header>
            <span>数据概览</span>
          </template>
          <div class="stats-list">
            <div class="stats-item">
              <span class="stats-label">宠物总数</span>
              <span class="stats-value">{{ userStats.pet_count || 0 }} 只</span>
            </div>
            <el-divider />
            <div class="stats-item">
              <span class="stats-label">疫苗记录</span>
              <span class="stats-value">{{ userStats.vaccination_count || 0 }} 条</span>
            </div>
            <el-divider />
            <div class="stats-item">
              <span class="stats-label">健康记录</span>
              <span class="stats-value">{{ userStats.health_record_count || 0 }} 条</span>
            </div>
            <el-divider />
            <div class="stats-item">
              <span class="stats-label">总消费</span>
              <span class="stats-value">¥{{ userStats.total_expense || 0 }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card class="info-card">
          <template #header>
            <span>基本信息</span>
            <el-button type="primary" size="small" @click="isEdit = !isEdit" v-if="!isEdit">
              编辑
            </el-button>
          </template>
          
          <el-form
            v-if="isEdit"
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" placeholder="请输入用户名" />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            
            <el-form-item label="真实姓名" prop="full_name">
              <el-input v-model="profileForm.full_name" placeholder="请输入真实姓名" />
            </el-form-item>
            
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="profileForm.phone" placeholder="请输入手机号码" />
            </el-form-item>
            
            <el-form-item label="出生日期" prop="birth_date">
              <el-date-picker
                v-model="profileForm.birth_date"
                type="date"
                placeholder="请选择出生日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
            
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="profileForm.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
                <el-radio label="unknown">保密</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="地址" prop="address">
              <el-input
                v-model="profileForm.address"
                type="textarea"
                :rows="2"
                placeholder="请输入联系地址"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button @click="isEdit = false">取消</el-button>
              <el-button type="primary" :loading="submitLoading" @click="handleSubmitProfile">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
          
          <el-descriptions :column="2" border v-else>
            <el-descriptions-item label="用户名">
              {{ userInfo.username }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ userInfo.email }}
            </el-descriptions-item>
            <el-descriptions-item label="真实姓名">
              {{ userInfo.full_name || '暂无' }}
            </el-descriptions-item>
            <el-descriptions-item label="手机号码">
              {{ userInfo.phone || '暂无' }}
            </el-descriptions-item>
            <el-descriptions-item label="出生日期">
              {{ userInfo.birth_date ? formatDate(userInfo.birth_date) : '暂无' }}
            </el-descriptions-item>
            <el-descriptions-item label="性别">
              {{ getGenderText(userInfo.gender) }}
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ formatDate(userInfo.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="最后登录时间">
              {{ userInfo.last_login ? formatDate(userInfo.last_login) : '暂无' }}
            </el-descriptions-item>
            <el-descriptions-item label="地址" :span="2">
              {{ userInfo.address || '暂无' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card class="password-card" style="margin-top: 20px">
          <template #header>
            <span>修改密码</span>
          </template>
          
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="120px"
          >
            <el-form-item label="当前密码" prop="old_password">
              <el-input
                v-model="passwordForm.old_password"
                type="password"
                placeholder="请输入当前密码"
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password">
              <el-input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="请输入新密码"
              />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input
                v-model="passwordForm.confirm_password"
                type="password"
                placeholder="请再次输入新密码"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="settings-card" style="margin-top: 20px">
          <template #header>
            <span>系统设置</span>
          </template>
          
          <el-form label-width="120px">
            <el-form-item label="邮件提醒">
              <el-switch v-model="settings.email_notification" />
              <span class="setting-desc">开启后将通过邮件提醒疫苗到期、复查等事项</span>
            </el-form-item>
            
            <el-form-item label="短信提醒">
              <el-switch v-model="settings.sms_notification" />
              <span class="setting-desc">开启后将通过短信提醒重要事项</span>
            </el-form-item>
            
            <el-form-item label="提前提醒天数">
              <el-input-number
                v-model="settings.remind_days"
                :min="1"
                :max="30"
                placeholder="提前提醒天数"
              />
              <span class="setting-desc">设置事项到期前提前提醒的天数</span>
            </el-form-item>
            
            <el-form-item label="语言设置">
              <el-select v-model="settings.language" style="width: 200px">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="主题设置">
              <el-radio-group v-model="settings.theme">
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
                <el-radio label="auto">跟随系统</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" :loading="settingsLoading" @click="handleSaveSettings">
                保存设置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, type FormInstance } from 'element-plus'
import { updateUserProfile, changePassword, getUserStats, updateUserSettings } from '@/api/user'
import { formatDate } from '@/utils/date'
import type { UpdateUserProfileDto, ChangePasswordDto, UpdateUserSettingsDto } from '@/types/user'

const userStore = useUserStore()
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const avatarUploadRef = ref<HTMLInputElement>()
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

const isEdit = ref(false)
const submitLoading = ref(false)
const passwordLoading = ref(false)
const settingsLoading = ref(false)

const userInfo = ref<any>({})
const userStats = ref({
  pet_count: 0,
  vaccination_count: 0,
  health_record_count: 0,
  total_expense: 0
})

const profileForm = reactive<UpdateUserProfileDto>({
  username: '',
  email: '',
  full_name: '',
  phone: '',
  birth_date: '',
  gender: '',
  address: ''
})

const passwordForm = reactive<ChangePasswordDto & { confirm_password: string }>({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const settings = reactive({
  email_notification: true,
  sms_notification: false,
  remind_days: 7,
  language: 'zh-CN',
  theme: 'light'
})

const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度在 6 到 32 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 获取用户信息
const fetchUserInfo = () => {
  userInfo.value = { ...userStore.userInfo }
  Object.assign(profileForm, {
    username: userInfo.value.username,
    email: userInfo.value.email,
    full_name: userInfo.value.full_name,
    phone: userInfo.value.phone,
    birth_date: userInfo.value.birth_date,
    gender: userInfo.value.gender,
    address: userInfo.value.address
  })
}

// 获取用户统计数据
const fetchUserStats = async () => {
  try {
    const res = await getUserStats()
    userStats.value = res.data
  } catch (error) {
    console.error('获取用户统计数据失败:', error)
  }
}

// 提交个人信息修改
const handleSubmitProfile = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        await updateUserProfile(profileForm)
        ElMessage.success('修改成功')
        isEdit.value = false
        await userStore.getUserInfo()
        fetchUserInfo()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '修改失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        const { confirm_password, ...passwordData } = passwordForm
        await changePassword(passwordData)
        ElMessage.success('密码修改成功，请重新登录')
        userStore.logout()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '密码修改失败')
      } finally {
        passwordLoading.value = false
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
        if (passwordFormRef.value) {
          passwordFormRef.value.resetFields()
        }
      }
    }
  })
}

// 头像上传
const handleAvatarUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  
  if (file.type.indexOf('image/') === -1) {
    ElMessage.error('请上传图片文件')
    return
  }
  
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }
  
  // 这里模拟头像上传，实际项目中需要上传到服务器
  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      // 这里应该调用上传头像的API
      // await uploadAvatar({ avatar: e.target?.result as string })
      userInfo.value.avatar = e.target?.result as string
      ElMessage.success('头像上传成功')
    } catch (error) {
      ElMessage.error('头像上传失败')
    }
  }
  reader.readAsDataURL(file)
}

// 保存设置
const handleSaveSettings = async () => {
  settingsLoading.value = true
  try {
    await updateUserSettings(settings as UpdateUserSettingsDto)
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败')
  } finally {
    settingsLoading.value = false
  }
}

// 获取性别文本
const getGenderText = (gender?: string) => {
  if (gender === 'male') return '男'
  if (gender === 'female') return '女'
  return '保密'
}

onMounted(() => {
  fetchUserInfo()
  fetchUserStats()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.avatar-card {
  text-align: center;
}

.avatar-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.user-basic {
  text-align: center;
}

.user-basic h3 {
  margin: 10px 0 5px;
  font-size: 20px;
}

.user-email {
  color: #909399;
  margin-bottom: 10px;
}

.stats-list {
  padding: 0 10px;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
}

.stats-label {
  color: #606266;
}

.stats-value {
  font-weight: bold;
  color: #303133;
}

.info-card :deep(.el-card__header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-desc {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}
</style>