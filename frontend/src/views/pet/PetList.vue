<template>
  <div class="pet-list-container">
    <div class="page-header">
      <h2>宠物档案管理</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        添加宠物
      </el-button>
    </div>

    <el-card class="pet-card-container">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :lg="8" v-for="pet in petList" :key="pet.id">
          <el-card class="pet-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <div class="card-title">
                  <p class="name">{{ pet.name }}</p>
                  <p class="subtitle">{{ pet.breed || '未填写品种' }}</p>
                </div>
                <el-dropdown @command="(command) => handleAction(command, pet)">
                  <el-button class="action-trigger" type="text" icon="MoreFilled" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>

            <div class="pet-profile">
              <div class="pet-avatar">
                <el-avatar :size="92" :src="pet.avatar || defaultAvatar">
                  {{ pet.name.charAt(0) }}
                </el-avatar>
              </div>
              <div class="pet-meta">
                <el-tag effect="light" size="small" round>
                  {{ pet.gender === '公' ? '公' : pet.gender === '母' ? '母' : '未知性别' }}
                </el-tag>
                <el-tag type="success" effect="light" size="small" round>
                  {{ calculateAge(pet.birth_date) }}
                </el-tag>
                <el-tag v-if="pet.weight" type="warning" effect="light" size="small" round>
                  {{ pet.weight }}kg
                </el-tag>
              </div>
            </div>

            <div class="pet-info-grid">
              <div class="info-item">
                <span class="label">品种：</span>
                <span class="value">{{ pet.breed || '未知' }}</span>
              </div>
              <div class="info-item">
                <span class="label">毛色：</span>
                <span class="value">{{ pet.color || '未知' }}</span>
              </div>
              <div class="info-item">
                <span class="label">生日：</span>
                <span class="value">{{ pet.birth_date ? formatDate(pet.birth_date) : '未知' }}</span>
              </div>
              <div class="info-item">
                <span class="label">芯片号：</span>
                <span class="value">{{ pet.chip_number || '未登记' }}</span>
              </div>
            </div>

            <div class="pet-actions">
              <el-button type="primary" class="action-btn" @click="viewPetDetail(pet)">
                查看详情
              </el-button>
              <el-button class="action-btn" @click="goToVaccine(pet)">
                疫苗记录
              </el-button>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="12" :lg="8" v-if="petList.length === 0">
          <div class="empty-pet">
            <el-empty description="暂无宠物档案，点击上方按钮添加您的爱宠吧" />
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 新增/编辑宠物弹窗 -->
    <el-dialog
      v-model="petDialogVisible"
      :title="isEdit ? '编辑宠物信息' : '添加宠物'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="petFormRef"
        :model="petForm"
        :rules="petRules"
        label-width="80px"
      >
        <el-form-item label="宠物名称" prop="name">
          <el-input v-model="petForm.name" placeholder="请输入宠物名称" />
        </el-form-item>

        <el-form-item label="品种" prop="breed">
          <el-input v-model="petForm.breed" placeholder="请输入品种" />
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-select v-model="petForm.gender" placeholder="请选择性别">
            <el-option label="公" value="公" />
            <el-option label="母" value="母" />
            <el-option label="未知" value="未知" />
          </el-select>
        </el-form-item>

        <el-form-item label="体重(kg)" prop="weight">
          <el-input-number v-model="petForm.weight" :min="0" :precision="2" :step="0.1" placeholder="请输入体重" />
        </el-form-item>

        <el-form-item label="毛色" prop="color">
          <el-input v-model="petForm.color" placeholder="请输入毛色" />
        </el-form-item>

        <el-form-item label="芯片号" prop="chip_number">
          <el-input v-model="petForm.chip_number" placeholder="请输入芯片号" />
        </el-form-item>

        <el-form-item label="性格特点" prop="personality">
          <el-input v-model="petForm.personality" type="textarea" :rows="2" placeholder="请输入性格特点" />
        </el-form-item>

        <el-form-item label="生日" prop="birth_date">
          <el-date-picker
            v-model="petForm.birth_date"
            type="date"
            placeholder="请选择生日"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="handleAvatarUpload"
          >
            <img v-if="petForm.avatar" :src="petForm.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="特征描述">
          <el-input
            v-model="petForm.description"
            type="textarea"
            :rows="2"
            placeholder="请输入特征描述"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="petDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmitPet">
          {{ isEdit ? '保存修改' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 宠物详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="宠物详情"
      width="600px"
    >
      <div v-if="currentPet" class="pet-detail">
        <div class="detail-header">
          <el-avatar :size="100" :src="currentPet.avatar || defaultAvatar">
            {{ currentPet.name.charAt(0) }}
          </el-avatar>
          <div class="detail-basic">
            <h3>{{ currentPet.name }}</h3>
            <div class="detail-tags">
              <el-tag size="small" type="info">{{ currentPet.breed || '未知品种' }}</el-tag>
              <el-tag size="small" type="success">{{ calculateAge(currentPet.birth_date) }}</el-tag>
              <el-tag v-if="currentPet.weight" size="small" type="warning">{{ currentPet.weight }}kg</el-tag>
            </div>
          </div>
        </div>

        <el-divider />

        <el-descriptions :column="2" border>
          <el-descriptions-item label="性别">
            {{ currentPet.gender || '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="毛色">
            {{ currentPet.color || '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="芯片号">
            {{ currentPet.chip_number || '未登记' }}
          </el-descriptions-item>
          <el-descriptions-item label="生日">
            {{ currentPet.birth_date ? formatDate(currentPet.birth_date) : '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(currentPet.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ formatDate(currentPet.updated_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="特征描述" :span="2">
            {{ currentPet.description || '暂无描述' }}
          </el-descriptions-item>
          <el-descriptions-item label="性格特点" :span="2">
            {{ currentPet.personality || '暂无记录' }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-stats">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="stat-item">
                <p class="stat-number">{{ currentPet.vaccination_count || 0 }}</p>
                <p class="stat-label">疫苗记录</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <p class="stat-number">{{ currentPet.health_record_count || 0 }}</p>
                <p class="stat-label">健康记录</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <p class="stat-number">¥{{ currentPet.total_expense || 0 }}</p>
                <p class="stat-label">总消费</p>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="editFromDetail">编辑信息</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
    >
      <p>确定要删除宠物 <strong>{{ currentPet?.name }}</strong> 的所有信息吗？此操作不可恢复。</p>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="deleteLoading" @click="confirmDelete">
          确认删除
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type UploadProps } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getPetList, createPet, updatePet, deletePet, getPetDetail } from '@/api/pet'
import { formatDate } from '@/utils/date'
import type { PetDto, CreatePetDto, UpdatePetDto } from '@/types/pet'

const router = useRouter()
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const petList = ref<PetDto[]>([])
const petDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const petFormRef = ref<FormInstance>()
const submitLoading = ref(false)
const deleteLoading = ref(false)
const isEdit = ref(false)
const currentPet = ref<PetDto | null>(null)

const petForm = reactive<CreatePetDto | UpdatePetDto>({
  name: '',
  breed: '',
  gender: '',
  birth_date: '',
  weight: undefined,
  color: '',
  chip_number: '',
  description: '',
  personality: '',
  avatar: ''
})

const petRules = {
  name: [
    { required: true, message: '请输入宠物名称', trigger: 'blur' },
    { min: 1, max: 50, message: '名称长度在 1 到 50 个字符', trigger: 'blur' }
  ]
}

const showFriendlyError = (error: any, fallback: string) => {
  const status = error?.response?.status
  const messageByStatus: Record<number, string> = {
    401: '登录状态已过期，请重新登录后再试',
    403: '当前账号暂无权限访问这部分数据',
    404: '请求的服务暂时不可用，请稍后刷新重试',
    500: '服务器开小差了，请稍后再试'
  }
  const backendError = error?.response?.data
  const backendMessage = backendError
    ? Object.entries(backendError)
        .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
        .join('; ')
    : ''
  const message = messageByStatus[status] || backendMessage || fallback
  ElMessage({
    type: 'error',
    showClose: true,
    duration: 3600,
    message
  })
}

// 获取宠物列表
const fetchPetList = async () => {
  try {
    const res = await getPetList()
    const payload = res as any
    if (Array.isArray(payload)) {
      petList.value = payload
      return
    }
    if (Array.isArray(payload?.results)) {
      petList.value = payload.results
      return
    }
    if (Array.isArray(payload?.data)) {
      petList.value = payload.data
      return
    }
    petList.value = []
  } catch (error: any) {
    showFriendlyError(error, '宠物列表加载失败，请稍后重试')
  }
}

// 打开创建弹窗
const openCreateDialog = () => {
  isEdit.value = false
  petDialogVisible.value = true
  Object.assign(petForm, {
    name: '',
    breed: '',
    gender: '',
    birth_date: '',
    weight: undefined,
    color: '',
    chip_number: '',
    description: '',
    personality: '',
    avatar: ''
  })
  if (petFormRef.value) {
    petFormRef.value.resetFields()
  }
}

// 打开编辑弹窗
const openEditDialog = (pet: PetDto) => {
  isEdit.value = true
  currentPet.value = pet
  petDialogVisible.value = true
  Object.assign(petForm, {
    name: pet.name,
    breed: pet.breed,
    gender: pet.gender,
    birth_date: pet.birth_date,
    weight: pet.weight,
    color: pet.color,
    chip_number: pet.chip_number,
    description: pet.description,
    personality: pet.personality,
    avatar: pet.avatar
  })
}

// 提交宠物信息
const handleSubmitPet = async () => {
  if (!petFormRef.value) return

  await petFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const payload: any = {
          name: (petForm as any).name,
          breed: (petForm as any).breed,
          gender: (petForm as any).gender,
          birth_date: (petForm as any).birth_date,
          weight: (petForm as any).weight,
          color: (petForm as any).color,
          chip_number: (petForm as any).chip_number,
          description: (petForm as any).description,
          personality: (petForm as any).personality
        }
        const avatarValue = (petForm as any).avatar as string | undefined
        if (avatarValue && avatarValue.startsWith('data:image')) {
          payload.avatar = avatarValue
        } else if (!isEdit.value && avatarValue === '') {
          payload.avatar = ''
        }

        if (isEdit.value && currentPet.value) {
          await updatePet(currentPet.value.id, payload as UpdatePetDto)
          ElMessage.success('修改成功')
        } else {
          await createPet(payload as CreatePetDto)
          ElMessage.success('添加成功')
        }
        await fetchPetList()
        petDialogVisible.value = false
      } catch (error: any) {
        showFriendlyError(error, '保存失败，请检查填写信息后重试')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 查看宠物详情
const viewPetDetail = async (pet: PetDto) => {
  try {
    const res = await getPetDetail(pet.id)
    currentPet.value = res as unknown as PetDto
    detailDialogVisible.value = true
  } catch (error: any) {
    showFriendlyError(error, '宠物详情加载失败，请稍后重试')
  }
}

// 从详情页编辑
const editFromDetail = () => {
  detailDialogVisible.value = false
  if (currentPet.value) {
    openEditDialog(currentPet.value)
  }
}

// 跳转疫苗记录
const goToVaccine = (pet: PetDto) => {
  router.push({ path: '/vaccinations', query: { pet_id: pet.id } })
}

// 操作菜单
const handleAction = (command: string, pet: PetDto) => {
  currentPet.value = pet
  if (command === 'edit') {
    openEditDialog(pet)
  } else if (command === 'delete') {
    deleteDialogVisible.value = true
  }
}

// 确认删除
const confirmDelete = async () => {
  if (!currentPet.value) return

  deleteLoading.value = true
  try {
    await deletePet(currentPet.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    await fetchPetList()
  } catch (error: any) {
    showFriendlyError(error, '删除失败，请稍后重试')
  } finally {
    deleteLoading.value = false
  }
}

// 头像上传前校验
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type.indexOf('image/') === -1) {
    ElMessage.error('请上传图片文件')
    return false
  }
  const isLt10M = rawFile.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
}

// 处理头像上传（转成 base64 交给后端）
const handleAvatarUpload = (options: any) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    petForm.avatar = e.target?.result as string
  }
  reader.readAsDataURL(options.file)
}

// 计算年龄
const calculateAge = (birthDate?: string) => {
  if (!birthDate) return '未知'
  const birth = new Date(birthDate)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const monthDiff = now.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
    age--
  }
  return `${age}岁`
}

onMounted(() => {
  fetchPetList()
})
</script>

<style scoped>
.pet-list-container {
  width: 100%;
  --pet-peach: #ffe8dc;
  --pet-cream: #fff8ef;
  --pet-mint: #e6f8ef;
  --pet-blue: #e9f2ff;
  --pet-text-main: #5b3a29;
  --pet-text-sub: #a17358;
}

.pet-card-container {
  min-height: 240px;
  border: 0;
  background:
    radial-gradient(circle at 15% 18%, rgba(255, 187, 132, 0.22) 0, rgba(255, 187, 132, 0) 28%),
    radial-gradient(circle at 84% 12%, rgba(162, 213, 255, 0.2) 0, rgba(162, 213, 255, 0) 26%),
    linear-gradient(150deg, #fffaf4 0%, #fef2ea 54%, #f9f8ff 100%);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2px 0;
}

.pet-card {
  margin-bottom: 20px;
  border: 0;
  border-radius: 20px;
  overflow: hidden;
  background: linear-gradient(180deg, #fffefc 0%, #fff6ec 100%);
  box-shadow: 0 12px 28px rgba(224, 158, 118, 0.2);
  transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
  position: relative;
}

.pet-card::before {
  content: '';
  position: absolute;
  top: -28px;
  right: -24px;
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 190, 144, 0.5) 0%, rgba(255, 190, 144, 0) 72%);
  pointer-events: none;
}

.pet-card:hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 18px 36px rgba(224, 158, 118, 0.28);
  filter: saturate(1.05);
}

.card-title .name {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--pet-text-main);
}

.card-title .subtitle {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--pet-text-sub);
}

.action-trigger {
  color: #9f6d4f;
}

.pet-profile {
  padding: 8px 0 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.pet-avatar {
  width: 108px;
  height: 108px;
  border-radius: 999px;
  padding: 8px;
  background: conic-gradient(from 130deg, var(--pet-peach), var(--pet-mint), var(--pet-blue), var(--pet-peach));
  box-shadow: inset 0 0 0 1px #f4d5c0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pet-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.pet-meta :deep(.el-tag) {
  border: 0;
  color: #8f5536;
  background: #fff1e4;
}

.pet-meta :deep(.el-tag.el-tag--success) {
  color: #2f8e65;
  background: #e8f9ef;
}

.pet-meta :deep(.el-tag.el-tag--warning) {
  color: #b66a28;
  background: #fff3de;
}

.pet-info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  padding: 12px 14px;
  background: linear-gradient(160deg, #fff6ec 0%, #fff9f2 100%);
  border-radius: 12px;
  border: 1px solid #f5d9c2;
}

.info-item {
  display: flex;
  align-items: center;
  min-width: 0;
}

.label {
  color: #aa7e63;
  font-size: 12px;
  flex-shrink: 0;
}

.value {
  color: #6f4733;
  font-size: 13px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pet-actions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  height: 36px;
  border-radius: 12px;
  font-weight: 600;
  border-color: #f0b894;
  color: #905230;
  background: #fff8f2;
}

.action-btn:hover {
  border-color: #e99f71;
  color: #7a4326;
  background: #ffeede;
}

.action-btn.el-button--primary {
  border: 0;
  color: #fff;
  background: linear-gradient(135deg, #ff9f67 0%, #ff7f88 100%);
  box-shadow: 0 8px 18px rgba(255, 136, 126, 0.35);
}

.action-btn.el-button--primary:hover {
  background: linear-gradient(135deg, #ff9457 0%, #ff6f7b 100%);
}

.avatar-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  width: 96px;
  height: 96px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s ease;
}

.avatar-uploader :deep(.el-upload:hover) {
  border-color: #409eff;
}

.avatar {
  width: 96px;
  height: 96px;
  object-fit: cover;
  display: block;
}

.avatar-uploader-icon {
  font-size: 24px;
  color: #8c939d;
}

.empty-pet {
  padding: 40px 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.detail-basic h3 {
  margin-bottom: 8px;
}

.detail-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-stats {
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  color: #909399;
}

@media (max-width: 768px) {
  .pet-info-grid {
    grid-template-columns: 1fr;
  }

  .pet-actions {
    flex-direction: column;
  }
}
</style>
