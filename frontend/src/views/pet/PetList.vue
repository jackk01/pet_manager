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
        <el-col :span="8" v-for="pet in petList" :key="pet.id">
          <el-card class="pet-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>{{ pet.name }}</span>
                <el-dropdown @command="(command) => handleAction(command, pet)">
                  <el-button type="text" icon="MoreFilled" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
            
            <div class="pet-avatar">
              <el-avatar :size="80" :src="pet.avatar || defaultAvatar">
                {{ pet.name.charAt(0) }}
              </el-avatar>
            </div>
            
            <div class="pet-info">
              <div class="info-row">
                <span class="label">品种：</span>
                <span class="value">{{ pet.breed || '未知' }}</span>
              </div>
              <div class="info-row">
                <span class="label">品种：</span>
                <span class="value">{{ pet.breed || '未知' }}</span>
              </div>
              <div class="info-row">
                <span class="label">性别：</span>
                <span class="value">
                  {{ pet.gender === 'male' ? '公' : pet.gender === 'female' ? '母' : '未知' }}
                </span>
              </div>
              <div class="info-row">
                <span class="label">生日：</span>
                <span class="value">{{ pet.birth_date ? formatDate(pet.birth_date) : '未知' }}</span>
              </div>
              <div class="info-row">
                <span class="label">年龄：</span>
                <span class="value">{{ calculateAge(pet.birth_date) }}</span>
              </div>
            </div>

            <div class="pet-actions">
              <el-button type="primary" size="small" @click="viewPetDetail(pet)">
                查看详情
              </el-button>
              <el-button size="small" @click="goToVaccine(pet)">
                疫苗记录
              </el-button>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8" v-if="petList.length === 0">
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
import { ElMessage, ElMessageBox, type FormInstance, type UploadProps } from 'element-plus'
import { Plus, MoreFilled } from '@element-plus/icons-vue'
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

// 获取宠物列表
const fetchPetList = async () => {
  try {
    const res = await getPetList()
    petList.value = res.data
  } catch (error) {
    ElMessage.error('获取宠物列表失败')
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
        if (isEdit.value && currentPet.value) {
          await updatePet(currentPet.value.id, petForm as UpdatePetDto)
          ElMessage.success('修改成功')
        } else {
          await createPet(petForm as CreatePetDto)
          ElMessage.success('添加成功')
        }
        petDialogVisible.value = false
        fetchPetList()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
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
    currentPet.value = res.data
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取宠物详情失败')
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
  router.push({ path: '/vaccination', query: { pet_id: pet.id } })
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
    fetchPetList()
  } catch (error) {
    ElMessage.error('删除失败')
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
  const isLt2M = rawFile.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }
  return true
}

// 处理头像上传（这里模拟上传，实际项目中需要上传到服务器）
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
</script>