<template>
  <div class="health-container">
    <div class="page-header">
      <h2>健康记录管理</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        添加健康记录
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-form :model="filterForm" inline class="filter-form">
        <el-form-item label="选择宠物">
          <el-select
            v-model="filterForm.pet_id"
            placeholder="全部宠物"
            clearable
            style="width: 180px"
            @change="fetchHealthList"
          >
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="记录类型">
          <el-select
            v-model="filterForm.record_type"
            placeholder="全部类型"
            clearable
            style="width: 180px"
            @change="fetchHealthList"
          >
            <el-option label="体检" value="体检" />
            <el-option label="看病" value="看病" />
            <el-option label="驱虫" value="驱虫" />
            <el-option label="美容" value="美容" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 300px"
            @change="fetchHealthList"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="healthList"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="pet_name" label="宠物名称" width="120">
          <template #default="scope">
            <el-avatar :size="32" :src="scope.row.pet_avatar" style="margin-right: 8px">
              {{ scope.row.pet_name?.charAt(0) }}
            </el-avatar>
            {{ scope.row.pet_name }}
          </template>
        </el-table-column>
        
        <el-table-column prop="record_type" label="记录类型" width="100">
          <template #default="scope">
            <el-tag size="small" :type="getRecordTypeTag(scope.row.record_type)">
              {{ scope.row.record_type }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="visit_date" label="就诊日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.visit_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="title" label="标题" width="200" />
        
        <el-table-column prop="description" label="症状描述" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="diagnosis" label="诊断结果" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="vet_name" label="兽医" width="100" />
        <el-table-column prop="clinic_name" label="医院" width="150" />
        <el-table-column prop="cost" label="花费" width="100">
          <template #default="scope">
            ¥{{ scope.row.cost || 0 }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" link @click="viewDetail(scope.row)">
              查看
            </el-button>
            <el-button type="primary" size="small" link @click="openEditDialog(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchHealthList"
          @current-change="fetchHealthList"
        />
      </div>
    </el-card>

    <!-- 新增/编辑健康记录弹窗 -->
    <el-dialog
      v-model="healthDialogVisible"
      :title="isEdit ? '编辑健康记录' : '添加健康记录'"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="healthFormRef"
        :model="healthForm"
        :rules="healthRules"
        label-width="100px"
      >
        <el-form-item label="选择宠物" prop="pet_id">
          <el-select v-model="healthForm.pet_id" placeholder="请选择宠物" style="width: 100%">
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="记录类型" prop="record_type">
          <el-select v-model="healthForm.record_type" placeholder="请选择记录类型" style="width: 100%">
            <el-option label="就诊" value="就诊" />
            <el-option label="体检" value="体检" />
            <el-option label="体重" value="体重" />
            <el-option label="驱虫" value="驱虫" />
            <el-option label="过敏" value="过敏" />
            <el-option label="手术" value="手术" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="标题" prop="title">
          <el-input v-model="healthForm.title" placeholder="请输入记录标题" />
        </el-form-item>
        
        <el-form-item label="记录日期" prop="record_date">
          <el-date-picker
            v-model="healthForm.record_date"
            type="date"
            placeholder="请选择记录日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="医生" prop="doctor">
              <el-input v-model="healthForm.doctor" placeholder="请输入医生姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="医院" prop="hospital">
              <el-input v-model="healthForm.hospital" placeholder="请输入医院名称" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="症状描述" prop="description">
          <el-input
            v-model="healthForm.description"
            type="textarea"
            :rows="3"
            placeholder="请描述症状"
          />
        </el-form-item>
        
        <el-form-item label="诊断结果" prop="diagnosis">
          <el-input
            v-model="healthForm.diagnosis"
            type="textarea"
            :rows="3"
            placeholder="请输入诊断结果"
          />
        </el-form-item>
        
        <el-form-item label="治疗方案" prop="treatment">
          <el-input
            v-model="healthForm.treatment"
            type="textarea"
            :rows="3"
            placeholder="请输入治疗方案"
          />
        </el-form-item>
        
        <el-form-item label="医嘱" prop="prescription">
          <el-input
            v-model="healthForm.prescription"
            type="textarea"
            :rows="3"
            placeholder="请输入医嘱"
          />
        </el-form-item>
        
        <el-form-item label="花费" prop="cost">
          <el-input-number
            v-model="healthForm.cost"
            :min="0"
            :precision="2"
            placeholder="请输入花费金额"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="下次复查日期" prop="next_visit_date">
          <el-date-picker
            v-model="healthForm.next_visit_date"
            type="date"
            placeholder="请选择下次复查日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="healthForm.notes"
            type="textarea"
            :rows="2"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="healthDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmitHealth">
          {{ isEdit ? '保存修改' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="健康记录详情"
      width="700px"
    >
      <div v-if="currentHealth" class="health-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="宠物名称">
            <el-avatar :size="32" :src="currentHealth.pet_avatar" style="margin-right: 8px">
              {{ currentHealth.pet_name?.charAt(0) }}
            </el-avatar>
            {{ currentHealth.pet_name }}
          </el-descriptions-item>
          <el-descriptions-item label="记录类型">
            <el-tag :type="getRecordTypeTag(currentHealth.record_type)" size="small">
              {{ currentHealth.record_type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="标题">
            {{ currentHealth.title }}
          </el-descriptions-item>
          <el-descriptions-item label="就诊日期">
            {{ formatDate(currentHealth.visit_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="兽医">
            {{ currentHealth.vet_name || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="医院">
            {{ currentHealth.clinic_name || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="花费">
            ¥{{ currentHealth.cost || 0 }}
          </el-descriptions-item>
          <el-descriptions-item label="下次复查日期">
            {{ currentHealth.next_visit_date ? formatDate(currentHealth.next_visit_date) : '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="症状描述" :span="2">
            {{ currentHealth.description || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="诊断结果" :span="2">
            {{ currentHealth.diagnosis || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="治疗方案" :span="2">
            {{ currentHealth.treatment || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="医嘱" :span="2">
            {{ currentHealth.prescription || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">
            {{ currentHealth.notes || '暂无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="editFromDetail">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
    >
      <p>确定要删除这条健康记录吗？此操作不可恢复。</p>
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
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getHealthRecordList, createHealthRecord, updateHealthRecord, deleteHealthRecord } from '@/api/health'
import { getPetList } from '@/api/pet'
import { formatDate } from '@/utils/date'
import type { HealthRecordDto, CreateHealthRecordDto, UpdateHealthRecordDto } from '@/types/health'
import type { PetDto } from '@/types/pet'

const healthList = ref<HealthRecordDto[]>([])
const petList = ref<PetDto[]>([])
const healthDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const healthFormRef = ref<FormInstance>()
const loading = ref(false)
const submitLoading = ref(false)
const deleteLoading = ref(false)
const isEdit = ref(false)
const currentHealth = ref<HealthRecordDto | null>(null)

const filterForm = reactive({
  pet_id: undefined as number | undefined,
  record_type: undefined as string | undefined,
  date_range: [] as string[] | undefined
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const healthForm = reactive<CreateHealthRecordDto | UpdateHealthRecordDto>({
  pet_id: undefined as number | undefined,
  record_type: '',
  record_date: '',
  title: '',
  content: '',
  doctor: '',
  hospital: '',
  cost: undefined,
  attachment: '',
  next_check_date: ''
})

const healthRules = {
  pet_id: [
    { required: true, message: '请选择宠物', trigger: 'change' }
  ],
  record_type: [
    { required: true, message: '请选择记录类型', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入记录标题', trigger: 'blur' }
  ],
  record_date: [
    { required: true, message: '请选择记录日期', trigger: 'change' }
  ]
}

const parseListPayload = <T>(payload: any): { items: T[]; total: number } => {
  if (Array.isArray(payload)) {
    return { items: payload, total: payload.length }
  }
  if (Array.isArray(payload?.results)) {
    return { items: payload.results, total: payload.count ?? payload.results.length }
  }
  if (Array.isArray(payload?.items)) {
    return { items: payload.items, total: payload.total ?? payload.items.length }
  }
  if (Array.isArray(payload?.data?.items)) {
    return { items: payload.data.items, total: payload.data.total ?? payload.data.items.length }
  }
  if (Array.isArray(payload?.data)) {
    return { items: payload.data, total: payload.data.length }
  }
  return { items: [], total: 0 }
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
    const parsed = parseListPayload<PetDto>(res as any)
    petList.value = parsed.items
  } catch (error: any) {
    showFriendlyError(error, '宠物列表加载失败，请稍后重试')
  }
}

// 获取健康记录列表
const fetchHealthList = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      size: pagination.size,
      pet_id: filterForm.pet_id,
      record_type: filterForm.record_type
    }
    
    if (filterForm.date_range && filterForm.date_range.length === 2) {
      params.start_date = filterForm.date_range[0]
      params.end_date = filterForm.date_range[1]
    }
    
    const res = await getHealthRecordList(params)
    const parsed = parseListPayload<any>(res as any)
    healthList.value = parsed.items.map((item) => ({
      ...item,
      pet_id: item.pet_id ?? item.pet,
      pet_name: item.pet_name ?? petList.value.find((p) => p.id === (item.pet_id ?? item.pet))?.name,
      pet_avatar: item.pet_avatar ?? petList.value.find((p) => p.id === (item.pet_id ?? item.pet))?.avatar
    }))
    pagination.total = parsed.total
  } catch (error: any) {
    showFriendlyError(error, '健康记录加载失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 打开创建弹窗
const openCreateDialog = () => {
  isEdit.value = false
  healthDialogVisible.value = true
  Object.assign(healthForm, {
    pet_id: filterForm.pet_id,
    record_type: '',
    record_date: '',
    title: '',
    content: '',
    doctor: '',
    hospital: '',
    cost: undefined,
    attachment: '',
    next_check_date: ''
  })
  if (healthFormRef.value) {
    healthFormRef.value.resetFields()
  }
}

// 打开编辑弹窗
const openEditDialog = (health: HealthRecordDto) => {
  isEdit.value = true
  currentHealth.value = health
  healthDialogVisible.value = true
  Object.assign(healthForm, {
    pet_id: health.pet_id,
    record_type: health.record_type,
    record_date: health.record_date,
    title: health.title,
    content: health.content,
    doctor: health.doctor,
    hospital: health.hospital,
    cost: health.cost,
    attachment: health.attachment,
    next_check_date: health.next_check_date
  })
}

// 提交健康记录
const handleSubmitHealth = async () => {
  if (!healthFormRef.value) return
  
  await healthFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const payload: any = {
          pet: (healthForm as any).pet_id,
          record_type: (healthForm as any).record_type,
          record_date: (healthForm as any).record_date,
          title: (healthForm as any).title,
          content: (healthForm as any).content || '',
          doctor: (healthForm as any).doctor || '',
          hospital: (healthForm as any).hospital || '',
          cost: (healthForm as any).cost,
          attachment: (healthForm as any).attachment || '',
          next_check_date: (healthForm as any).next_check_date || undefined
        }
        if (isEdit.value && currentHealth.value) {
          await updateHealthRecord(currentHealth.value.id, payload as UpdateHealthRecordDto)
          ElMessage.success('修改成功')
        } else {
          await createHealthRecord(payload as CreateHealthRecordDto)
          ElMessage.success('添加成功')
        }
        healthDialogVisible.value = false
        await fetchHealthList()
      } catch (error: any) {
        showFriendlyError(error, '保存失败，请检查填写信息后重试')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 查看详情
const viewDetail = (health: HealthRecordDto) => {
  currentHealth.value = health
  detailDialogVisible.value = true
}

// 从详情页编辑
const editFromDetail = () => {
  detailDialogVisible.value = false
  if (currentHealth.value) {
    openEditDialog(currentHealth.value)
  }
}

// 删除操作
const handleDelete = (health: HealthRecordDto) => {
  currentHealth.value = health
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!currentHealth.value) return
  
  deleteLoading.value = true
  try {
    await deleteHealthRecord(currentHealth.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    await fetchHealthList()
  } catch (error: any) {
    showFriendlyError(error, '删除失败，请稍后重试')
  } finally {
    deleteLoading.value = false
  }
}

// 获取记录类型标签颜色
const getRecordTypeTag = (type: string) => {
  if (type === '就诊') return 'danger'
  if (type === '体检') return 'primary'
  if (type === '体重') return 'success'
  if (type === '驱虫') return 'success'
  if (type === '过敏') return 'warning'
  if (type === '手术') return 'danger'
  return 'info'
}

onMounted(async () => {
  await fetchPetList()
  await fetchHealthList()
})
</script>
