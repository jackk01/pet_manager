<template>
  <div class="vaccination-container">
    <div class="page-header">
      <h2>疫苗管理</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        添加疫苗记录
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
            @change="fetchVaccinationList"
          >
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="接种状态">
          <el-select
            v-model="filterForm.status"
            placeholder="全部状态"
            clearable
            style="width: 180px"
            @change="fetchVaccinationList"
          >
            <el-option label="已接种" value="completed" />
            <el-option label="未接种" value="pending" />
            <el-option label="已过期" value="expired" />
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
            @change="fetchVaccinationList"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="vaccinationList"
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
        
        <el-table-column prop="vaccine_name" label="疫苗名称" width="180" />
        
        <el-table-column prop="vaccination_date" label="接种日期" width="120">
          <template #default="scope">
            {{ scope.row.vaccination_date ? formatDate(scope.row.vaccination_date) : '-' }}
          </template>
        </el-table-column>
        
        <el-table-column prop="next_due_date" label="下次到期日" width="120">
          <template #default="scope">
            <span :class="getDueDateClass(scope.row.next_due_date)">
              {{ scope.row.next_due_date ? formatDate(scope.row.next_due_date) : '无需再次接种' }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="clinic" label="接种单位" width="150" />
        <el-table-column prop="doctor" label="医生" width="100" />
        <el-table-column prop="batch_number" label="批号" width="120" />
        <el-table-column prop="remark" label="备注" width="150" />
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
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
          @size-change="fetchVaccinationList"
          @current-change="fetchVaccinationList"
        />
      </div>
    </el-card>

    <!-- 新增/编辑疫苗记录弹窗 -->
    <el-dialog
      v-model="vaccineDialogVisible"
      :title="isEdit ? '编辑疫苗记录' : '添加疫苗记录'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="vaccineFormRef"
        :model="vaccineForm"
        :rules="vaccineRules"
        label-width="100px"
      >
        <el-form-item label="选择宠物" prop="pet_id">
          <el-select v-model="vaccineForm.pet_id" placeholder="请选择宠物" style="width: 100%">
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="疫苗名称" prop="vaccine_name">
          <el-input v-model="vaccineForm.vaccine_name" placeholder="请输入疫苗名称" />
        </el-form-item>
        
        <el-form-item label="疫苗类型" prop="vaccine_type">
          <el-select v-model="vaccineForm.vaccine_type" placeholder="请选择疫苗类型" style="width: 100%">
            <el-option label="核心疫苗" value="核心疫苗" />
            <el-option label="非核心疫苗" value="非核心疫苗" />
            <el-option label="狂犬疫苗" value="狂犬疫苗" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="接种日期" prop="vaccination_date">
              <el-date-picker
                v-model="vaccineForm.vaccination_date"
                type="date"
                placeholder="请选择接种日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="下次到期日" prop="next_due_date">
              <el-date-picker
                v-model="vaccineForm.next_due_date"
                type="date"
                placeholder="请选择下次到期日"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="批号" prop="batch_number">
              <el-input v-model="vaccineForm.batch_number" placeholder="请输入批号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="接种单位" prop="clinic">
              <el-input v-model="vaccineForm.clinic" placeholder="请输入接种单位" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="医生" prop="doctor">
          <el-input v-model="vaccineForm.doctor" placeholder="请输入医生姓名" />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="vaccineForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="vaccineDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmitVaccine">
          {{ isEdit ? '保存修改' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
    >
      <p>确定要删除这条疫苗记录吗？此操作不可恢复。</p>
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
import { useRoute } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getVaccinationList, createVaccination, updateVaccination, deleteVaccination } from '@/api/vaccination'
import { getPetList } from '@/api/pet'
import { formatDate } from '@/utils/date'
import type { VaccinationDto, CreateVaccinationDto, UpdateVaccinationDto } from '@/types/vaccination'
import type { PetDto } from '@/types/pet'

const route = useRoute()

const vaccinationList = ref<VaccinationDto[]>([])
const petList = ref<PetDto[]>([])
const vaccineDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const vaccineFormRef = ref<FormInstance>()
const loading = ref(false)
const submitLoading = ref(false)
const deleteLoading = ref(false)
const isEdit = ref(false)
const currentVaccine = ref<VaccinationDto | null>(null)

const filterForm = reactive({
  pet_id: undefined as number | undefined,
  status: undefined as string | undefined,
  date_range: [] as string[] | undefined
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const vaccineForm = reactive<CreateVaccinationDto | UpdateVaccinationDto>({
  pet_id: undefined as number | undefined,
  vaccine_name: '',
  vaccination_date: '',
  next_due_date: '',
  batch_number: '',
  clinic: '',
  doctor: '',
  remark: '',
  attachment: ''
})

const vaccineRules = {
  pet_id: [
    { required: true, message: '请选择宠物', trigger: 'change' }
  ],
  vaccine_name: [
    { required: true, message: '请输入疫苗名称', trigger: 'blur' }
  ],
  vaccination_date: [
    { required: true, message: '请选择接种日期', trigger: 'change' }
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

const getDueDateClass = (nextDueDate?: string) => {
  if (!nextDueDate) return 'normal'
  const today = new Date()
  const due = new Date(nextDueDate)
  const diff = Math.ceil((due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  if (diff < 0) return 'expired'
  if (diff <= 30) return 'warning'
  return 'normal'
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

// 获取疫苗记录列表
const fetchVaccinationList = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      size: pagination.size,
      pet_id: filterForm.pet_id,
      status: filterForm.status
    }
    
    if (filterForm.date_range && filterForm.date_range.length === 2) {
      params.start_date = filterForm.date_range[0]
      params.end_date = filterForm.date_range[1]
    }
    
    const res = await getVaccinationList(params)
    const parsed = parseListPayload<any>(res as any)
    vaccinationList.value = parsed.items.map((item) => ({
      ...item,
      pet_id: item.pet_id ?? item.pet,
      pet_name: item.pet_name ?? petList.value.find((p) => p.id === (item.pet_id ?? item.pet))?.name,
      pet_avatar: item.pet_avatar ?? petList.value.find((p) => p.id === (item.pet_id ?? item.pet))?.avatar
    }))
    pagination.total = parsed.total
  } catch (error: any) {
    showFriendlyError(error, '疫苗记录加载失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 打开创建弹窗
const openCreateDialog = () => {
  isEdit.value = false
  vaccineDialogVisible.value = true
  Object.assign(vaccineForm, {
    pet_id: filterForm.pet_id,
    vaccine_name: '',
    vaccination_date: '',
    next_due_date: '',
    batch_number: '',
    clinic: '',
    doctor: '',
    remark: '',
    attachment: ''
  })
  if (vaccineFormRef.value) {
    vaccineFormRef.value.resetFields()
  }
}

// 打开编辑弹窗
const openEditDialog = (vaccine: VaccinationDto) => {
  isEdit.value = true
  currentVaccine.value = vaccine
  vaccineDialogVisible.value = true
  Object.assign(vaccineForm, {
    pet_id: vaccine.pet_id,
    vaccine_name: vaccine.vaccine_name,
    vaccination_date: vaccine.vaccination_date,
    next_due_date: vaccine.next_due_date,
    batch_number: vaccine.batch_number,
    clinic: vaccine.clinic,
    doctor: vaccine.doctor,
    remark: vaccine.remark,
    attachment: vaccine.attachment
  })
}

// 提交疫苗记录
const handleSubmitVaccine = async () => {
  if (!vaccineFormRef.value) return
  
  await vaccineFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const payload: any = {
          pet: (vaccineForm as any).pet_id,
          vaccine_name: (vaccineForm as any).vaccine_name,
          vaccination_date: (vaccineForm as any).vaccination_date,
          next_due_date: (vaccineForm as any).next_due_date || undefined,
          batch_number: (vaccineForm as any).batch_number || '',
          clinic: (vaccineForm as any).clinic || '',
          doctor: (vaccineForm as any).doctor || '',
          remark: (vaccineForm as any).remark || '',
          attachment: (vaccineForm as any).attachment || ''
        }
        if (isEdit.value && currentVaccine.value) {
          await updateVaccination(currentVaccine.value.id, payload as UpdateVaccinationDto)
          ElMessage.success('修改成功')
        } else {
          await createVaccination(payload as CreateVaccinationDto)
          ElMessage.success('添加成功')
        }
        vaccineDialogVisible.value = false
        await fetchVaccinationList()
      } catch (error: any) {
        showFriendlyError(error, '保存失败，请检查填写信息后重试')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 删除操作
const handleDelete = (vaccine: VaccinationDto) => {
  currentVaccine.value = vaccine
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!currentVaccine.value) return
  
  deleteLoading.value = true
  try {
    await deleteVaccination(currentVaccine.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    await fetchVaccinationList()
  } catch (error: any) {
    showFriendlyError(error, '删除失败，请稍后重试')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(async () => {
  const queryPetId = route.query.pet_id ? Number(route.query.pet_id) : undefined
  if (queryPetId && Number.isFinite(queryPetId)) {
    filterForm.pet_id = queryPetId
  }
  await fetchPetList()
  await fetchVaccinationList()
})
</script>
