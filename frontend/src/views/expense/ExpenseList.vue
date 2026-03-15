<template>
  <div class="expense-container">
    <div class="page-header">
      <h2>消费记录管理</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        添加消费记录
      </el-button>
    </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">本月总消费</p>
              <p class="stat-value">¥{{ stats.monthly_total || 0 }}</p>
            </div>
            <div class="stat-icon">
              <el-icon size="40" color="#f56c6c"><Money /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">年度总消费</p>
              <p class="stat-value">¥{{ stats.yearly_total || 0 }}</p>
            </div>
            <div class="stat-icon">
              <el-icon size="40" color="#409eff"><TrendCharts /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">平均每月消费</p>
              <p class="stat-value">¥{{ stats.average_monthly || 0 }}</p>
            </div>
            <div class="stat-icon">
              <el-icon size="40" color="#67c23a"><Calculator /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">累计总消费</p>
              <p class="stat-value">¥{{ stats.total || 0 }}</p>
            </div>
            <div class="stat-icon">
              <el-icon size="40" color="#e6a23c"><Coin /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="filter-card">
      <el-form :model="filterForm" inline class="filter-form">
        <el-form-item label="选择宠物">
          <el-select
            v-model="filterForm.pet_id"
            placeholder="全部宠物"
            clearable
            style="width: 180px"
            @change="fetchExpenseList"
          >
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="消费类型">
          <el-select
            v-model="filterForm.expense_type"
            placeholder="全部类型"
            clearable
            style="width: 180px"
            @change="fetchExpenseList"
          >
            <el-option label="食品" value="食品" />
            <el-option label="医疗" value="医疗" />
            <el-option label="美容" value="美容" />
            <el-option label="疫苗" value="疫苗" />
            <el-option label="玩具" value="玩具" />
            <el-option label="用品" value="用品" />
            <el-option label="寄养" value="寄养" />
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
            @change="fetchExpenseList"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="expenseList"
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
        
        <el-table-column prop="expense_type" label="消费类型" width="100">
          <template #default="scope">
            <el-tag size="small" :type="getExpenseTypeTag(scope.row.expense_type)">
              {{ scope.row.expense_type }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="expense_date" label="消费日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.expense_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="amount" label="金额" width="100" align="right">
          <template #default="scope">
            <span style="color: #f56c6c">¥{{ scope.row.amount }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="description" label="消费描述" min-width="200" />
        <el-table-column prop="merchant" label="商家" width="150" />
        <el-table-column prop="payment_method" label="支付方式" width="100">
          <template #default="scope">
            {{ getPaymentMethodText(scope.row.payment_method) }}
          </template>
        </el-table-column>
        
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
          @size-change="fetchExpenseList"
          @current-change="fetchExpenseList"
        />
      </div>
    </el-card>

    <!-- 新增/编辑消费记录弹窗 -->
    <el-dialog
      v-model="expenseDialogVisible"
      :title="isEdit ? '编辑消费记录' : '添加消费记录'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="expenseFormRef"
        :model="expenseForm"
        :rules="expenseRules"
        label-width="100px"
      >
        <el-form-item label="选择宠物" prop="pet_id">
          <el-select v-model="expenseForm.pet_id" placeholder="请选择宠物" style="width: 100%">
            <el-option
              v-for="pet in petList"
              :key="pet.id"
              :label="pet.name"
              :value="pet.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="消费分类" prop="category">
          <el-select v-model="expenseForm.category" placeholder="请选择消费分类" style="width: 100%">
            <el-option label="食品" value="food" />
            <el-option label="医疗" value="medical" />
            <el-option label="美容" value="grooming" />
            <el-option label="用品" value="supplies" />
            <el-option label="保险" value="insurance" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="消费金额" prop="amount">
          <el-input-number
            v-model="expenseForm.amount"
            :min="0"
            :precision="2"
            placeholder="请输入消费金额"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="消费日期" prop="expense_date">
          <el-date-picker
            v-model="expenseForm.expense_date"
            type="date"
            placeholder="请选择消费日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="商家" prop="merchant">
          <el-input v-model="expenseForm.merchant" placeholder="请输入商家名称" />
        </el-form-item>
        
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="expenseForm.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="expenseDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmitExpense">
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
      <p>确定要删除这条消费记录吗？此操作不可恢复。</p>
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
import { Plus, Money, TrendCharts, Calculator, Coin } from '@element-plus/icons-vue'
import { getExpenseList, createExpense, updateExpense, deleteExpense, getExpenseStats } from '@/api/expense'
import { getPetList } from '@/api/pet'
import { formatDate } from '@/utils/date'
import type { ExpenseDto, CreateExpenseDto, UpdateExpenseDto } from '@/types/expense'
import type { PetDto } from '@/types/pet'

const expenseList = ref<ExpenseDto[]>([])
const petList = ref<PetDto[]>([])
const stats = ref({
  monthly_total: 0,
  yearly_total: 0,
  average_monthly: 0,
  total: 0
})

const expenseDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const expenseFormRef = ref<FormInstance>()
const loading = ref(false)
const submitLoading = ref(false)
const deleteLoading = ref(false)
const isEdit = ref(false)
const currentExpense = ref<ExpenseDto | null>(null)

const filterForm = reactive({
  pet_id: undefined as number | undefined,
  expense_type: undefined as string | undefined,
  date_range: [] as string[] | undefined
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const expenseForm = reactive<CreateExpenseDto | UpdateExpenseDto>({
  pet_id: undefined as number | undefined,
  expense_type: '',
  amount: 0,
  expense_date: '',
  description: '',
  merchant: '',
  payment_method: '',
  notes: ''
})

const expenseRules = {
  pet_id: [
    { required: true, message: '请选择宠物', trigger: 'change' }
  ],
  expense_type: [
    { required: true, message: '请选择消费类型', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入消费金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '金额必须大于0', trigger: 'blur' }
  ],
  expense_date: [
    { required: true, message: '请选择消费日期', trigger: 'change' }
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

// 获取统计数据
const fetchStats = async () => {
  try {
    const res = await getExpenseStats()
    stats.value = res.data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取消费记录列表
const fetchExpenseList = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      size: pagination.size,
      pet_id: filterForm.pet_id,
      expense_type: filterForm.expense_type
    }
    
    if (filterForm.date_range && filterForm.date_range.length === 2) {
      params.start_date = filterForm.date_range[0]
      params.end_date = filterForm.date_range[1]
    }
    
    const res = await getExpenseList(params)
    expenseList.value = res.data.items
    pagination.total = res.data.total
  } catch (error) {
    ElMessage.error('获取消费记录失败')
  } finally {
    loading.value = false
  }
}

// 打开创建弹窗
const openCreateDialog = () => {
  isEdit.value = false
  expenseDialogVisible.value = true
  Object.assign(expenseForm, {
    pet_id: filterForm.pet_id,
    expense_type: '',
    amount: 0,
    expense_date: '',
    description: '',
    merchant: '',
    payment_method: '',
    notes: ''
  })
  if (expenseFormRef.value) {
    expenseFormRef.value.resetFields()
  }
}

// 打开编辑弹窗
const openEditDialog = (expense: ExpenseDto) => {
  isEdit.value = true
  currentExpense.value = expense
  expenseDialogVisible.value = true
  Object.assign(expenseForm, {
    pet_id: expense.pet_id,
    expense_type: expense.expense_type,
    amount: expense.amount,
    expense_date: expense.expense_date,
    description: expense.description,
    merchant: expense.merchant,
    payment_method: expense.payment_method,
    notes: expense.notes
  })
}

// 提交消费记录
const handleSubmitExpense = async () => {
  if (!expenseFormRef.value) return
  
  await expenseFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value && currentExpense.value) {
          await updateExpense(currentExpense.value.id, expenseForm as UpdateExpenseDto)
          ElMessage.success('修改成功')
        } else {
          await createExpense(expenseForm as CreateExpenseDto)
          ElMessage.success('添加成功')
        }
        expenseDialogVisible.value = false
        fetchExpenseList()
        fetchStats()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 删除操作
const handleDelete = (expense: ExpenseDto) => {
  currentExpense.value = expense
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!currentExpense.value) return
  
  deleteLoading.value = true
  try {
    await deleteExpense(currentExpense.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    fetchExpenseList()
    fetchStats()
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    deleteLoading.value = false
  }
}

// 获取消费类型标签颜色
const getExpenseTypeTag = (type: string) => {
  if (type === '食品') return 'primary'
  if (type === '医疗') return 'danger'
  if (type === '美容') return 'warning'
  if (type === '疫苗') return 'success'
  if (type === '玩具') return 'info'
  if (type === '用品') return 'primary'
  if (type === '寄养') return 'success'
  return 'info'
}

// 获取支付方式文本
const getPaymentMethodText = (method?: string) => {
  const methods: Record<string, string> = {
    wechat: '微信',
    alipay: '支付宝',
    cash: '现金',
    card: '银行卡',
    other: '其他'
  }
  return method ? methods[method] || '其他' : '其他'
}

onMounted(() => {
  fetchPetList()
  fetchExpenseList()
  fetchStats()
})
</script>