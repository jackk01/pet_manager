<template>
  <div class="statistics-container">
    <div class="page-header">
      <h2>数据统计分析</h2>
      <div class="header-actions">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchStatistics"
        />
        <el-select v-model="selectedPetId" placeholder="全部宠物" clearable @change="fetchStatistics">
          <el-option
            v-for="pet in petList"
            :key="pet.id"
            :label="pet.name"
            :value="pet.id"
          />
        </el-select>
      </div>
    </div>

    <el-row :gutter="20" class="overview-row">
      <el-col :span="6">
        <el-card class="overview-card">
          <div class="overview-content">
            <div class="overview-info">
              <p class="overview-label">总消费金额</p>
              <p class="overview-value">¥{{ stats.total_expense || 0 }}</p>
            </div>
            <div class="overview-icon expense-icon">
              <el-icon size="40"><Money /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="overview-card">
          <div class="overview-content">
            <div class="overview-info">
              <p class="overview-label">平均每月消费</p>
              <p class="overview-value">¥{{ stats.avg_monthly_expense || 0 }}</p>
            </div>
            <div class="overview-icon avg-icon">
              <el-icon size="40"><TrendCharts /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="overview-card">
          <div class="overview-content">
            <div class="overview-info">
              <p class="overview-label">疫苗接种次数</p>
              <p class="overview-value">{{ stats.total_vaccinations || 0 }}</p>
            </div>
            <div class="overview-icon vaccine-icon">
              <el-icon size="40"><Tools /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="overview-card">
          <div class="overview-content">
            <div class="overview-info">
              <p class="overview-label">健康记录数</p>
              <p class="overview-value">{{ stats.total_health_records || 0 }}</p>
            </div>
            <div class="overview-icon health-icon">
              <el-icon size="40"><FirstAidKit /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>月度消费趋势</span>
          </template>
          <div ref="monthlyTrendRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>消费类型分布</span>
          </template>
          <div ref="expenseTypeRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>宠物消费占比</span>
          </template>
          <div ref="petExpenseRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>健康记录类型分布</span>
          </template>
          <div ref="healthTypeRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <span>年度消费明细</span>
          </template>
          <div ref="yearlyDetailRef" class="chart-container bar-chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getStatistics } from '@/api/statistics'
import { getPetList } from '@/api/pet'
import { Money, TrendCharts, Tools, FirstAidKit } from '@element-plus/icons-vue'

const monthlyTrendRef = ref<HTMLElement>()
const expenseTypeRef = ref<HTMLElement>()
const petExpenseRef = ref<HTMLElement>()
const healthTypeRef = ref<HTMLElement>()
const yearlyDetailRef = ref<HTMLElement>()

let monthlyTrendChart: echarts.ECharts | null = null
let expenseTypeChart: echarts.ECharts | null = null
let petExpenseChart: echarts.ECharts | null = null
let healthTypeChart: echarts.ECharts | null = null
let yearlyDetailChart: echarts.ECharts | null = null

const petList = ref<any[]>([])
const dateRange = ref<string[]>([])
const selectedPetId = ref<number>()
const stats = ref<any>({})

// 获取宠物列表
const fetchPetList = async () => {
  try {
    const res = await getPetList()
    petList.value = res.data
  } catch (error) {
    console.error('获取宠物列表失败:', error)
  }
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const params: any = {}
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    if (selectedPetId.value) {
      params.pet_id = selectedPetId.value
    }
    
    const res = await getStatistics(params)
    stats.value = res.data
    initCharts()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 初始化所有图表
const initCharts = () => {
  initMonthlyTrendChart()
  initExpenseTypeChart()
  initPetExpenseChart()
  initHealthTypeChart()
  initYearlyDetailChart()
}

// 月度消费趋势图
const initMonthlyTrendChart = () => {
  if (!monthlyTrendRef.value) return
  
  monthlyTrendChart = echarts.init(monthlyTrendRef.value)
  
  const data = stats.value.monthly_trend || { months: [], amounts: [] }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>消费: ¥{c}'
    },
    xAxis: {
      type: 'category',
      data: data.months || [],
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '¥{value}'
      }
    },
    series: [
      {
        data: data.amounts || [],
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#409eff'
        },
        itemStyle: {
          color: '#409eff'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
          ])
        }
      }
    ]
  }
  
  monthlyTrendChart.setOption(option)
}

// 消费类型分布图
const initExpenseTypeChart = () => {
  if (!expenseTypeRef.value) return
  
  expenseTypeChart = echarts.init(expenseTypeRef.value)
  
  const data = stats.value.expense_type_distribution || []
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '消费类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map((item: any) => ({
          name: item.type,
          value: item.amount,
          itemStyle: {
            color: getTypeColor(item.type)
          }
        }))
      }
    ]
  }
  
  expenseTypeChart.setOption(option)
}

// 宠物消费占比图
const initPetExpenseChart = () => {
  if (!petExpenseRef.value) return
  
  petExpenseChart = echarts.init(petExpenseRef.value)
  
  const data = stats.value.pet_expense_distribution || []
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '宠物消费',
        type: 'pie',
        radius: '60%',
        data: data.map((item: any, index: number) => ({
          name: item.pet_name,
          value: item.amount,
          itemStyle: {
            color: ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#9c27b0'][index % 6]
          }
        }))
      }
    ]
  }
  
  petExpenseChart.setOption(option)
}

// 健康记录类型分布图
const initHealthTypeChart = () => {
  if (!healthTypeRef.value) return
  
  healthTypeChart = echarts.init(healthTypeRef.value)
  
  const data = stats.value.health_type_distribution || []
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '健康记录类型',
        type: 'pie',
        radius: ['40%', '70%'],
        roseType: 'radius',
        itemStyle: {
          borderRadius: 8
        },
        data: data.map((item: any) => ({
          name: item.type,
          value: item.count,
          itemStyle: {
            color: getHealthTypeColor(item.type)
          }
        }))
      }
    ]
  }
  
  healthTypeChart.setOption(option)
}

// 年度消费明细柱状图
const initYearlyDetailChart = () => {
  if (!yearlyDetailRef.value) return
  
  yearlyDetailChart = echarts.init(yearlyDetailRef.value)
  
  const data = stats.value.yearly_detail || { months: [], food: [], medical: [], beauty: [], other: [] }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['食品', '医疗', '美容', '其他']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.months || []
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '食品',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: data.food || [],
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '医疗',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: data.medical || [],
        itemStyle: {
          color: '#f56c6c'
        }
      },
      {
        name: '美容',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: data.beauty || [],
        itemStyle: {
          color: '#e6a23c'
        }
      },
      {
        name: '其他',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: data.other || [],
        itemStyle: {
          color: '#909399'
        }
      }
    ]
  }
  
  yearlyDetailChart.setOption(option)
}

// 获取消费类型颜色
const getTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    '食品': '#409eff',
    '医疗': '#f56c6c',
    '美容': '#e6a23c',
    '疫苗': '#67c23a',
    '玩具': '#909399',
    '用品': '#9c27b0',
    '寄养': '#67c23a',
    '其他': '#909399'
  }
  return colors[type] || '#409eff'
}

// 获取健康类型颜色
const getHealthTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    '体检': '#409eff',
    '看病': '#f56c6c',
    '驱虫': '#67c23a',
    '美容': '#e6a23c',
    '其他': '#909399'
  }
  return colors[type] || '#409eff'
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  monthlyTrendChart?.resize()
  expenseTypeChart?.resize()
  petExpenseChart?.resize()
  healthTypeChart?.resize()
  yearlyDetailChart?.resize()
}

onMounted(() => {
  fetchPetList()
  fetchStatistics()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  monthlyTrendChart?.dispose()
  expenseTypeChart?.dispose()
  petExpenseChart?.dispose()
  healthTypeChart?.dispose()
  yearlyDetailChart?.dispose()
})
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.overview-row {
  margin-bottom: 20px;
}

.overview-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.overview-content {
  display: flex;
  justify-content