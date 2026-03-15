<template>
  <div class="dashboard-container">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card pet-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">宠物总数</p>
              <p class="stat-value">{{ dashboardStats.pet_count || 0 }}</p>
              <p class="stat-change">
                <span :class="dashboardStats.pet_count > 0 ? 'increase' : ''">
                  {{ dashboardStats.pet_count > 0 ? '+' : '' }}{{ dashboardStats.pet_count }}
                </span>
                只宠物
              </p>
            </div>
            <div class="stat-icon">
              <el-icon size="48" color="#409eff"><House /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card vaccine-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">即将到期疫苗</p>
              <p class="stat-value">{{ dashboardStats.upcoming_vaccinations_count || 0 }}</p>
              <p class="stat-change">
                <span :class="dashboardStats.upcoming_vaccinations_count > 0 ? 'warning' : 'normal'">
                  {{ dashboardStats.upcoming_vaccinations_count }}
                </span>
                项需要注意
              </p>
            </div>
            <div class="stat-icon">
              <el-icon size="48" color="#e6a23c"><Tools /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card health-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">健康记录</p>
              <p class="stat-value">{{ dashboardStats.health_record_count || 0 }}</p>
              <p class="stat-change">
                <span class="increase">+{{ dashboardStats.monthly_health_records || 0 }}</span>
                本月新增
              </p>
            </div>
            <div class="stat-icon">
              <el-icon size="48" color="#67c23a"><FirstAidKit /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card expense-card">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-label">本月总消费</p>
              <p class="stat-value">¥{{ dashboardStats.monthly_total_expense || 0 }}</p>
              <p class="stat-change">
                <span :class="dashboardStats.expense_trend > 0 ? 'increase' : 'decrease'">
                  {{ dashboardStats.expense_trend > 0 ? '+' : '' }}{{ dashboardStats.expense_trend }}%
                </span>
                较上月
              </p>
            </div>
            <div class="stat-icon">
              <el-icon size="48" color="#f56c6c"><Money /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card title="近6个月消费趋势" class="chart-card">
          <div ref="expenseChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card title="消费类型分布" class="chart-card">
          <div ref="expenseTypeChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="reminder-row">
      <el-col :span="12">
        <el-card title="即将到期的疫苗提醒" class="reminder-card">
          <el-timeline v-if="upcomingVaccinations.length > 0">
            <el-timeline-item
              v-for="item in upcomingVaccinations"
              :key="item.id"
              timestamp="即将到期"
              color="warning"
            >
              <div class="reminder-item">
                <span class="pet-name">{{ item.pet_name }}</span>
                <span class="vaccine-name">需要接种 {{ item.vaccine_name }}</span>
                <span class="due-date">到期时间: {{ formatDate(item.due_date) }}</span>
              </div>
            </el-timeline-item>
          </el-timeline>
          <div v-else class="empty-reminder">
            <el-empty description="近期没有需要接种的疫苗" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card title="最近的健康记录" class="reminder-card">
          <el-timeline v-if="recentHealthRecords.length > 0">
            <el-timeline-item
              v-for="record in recentHealthRecords"
              :key="record.id"
              :timestamp="formatDate(record.visit_date)"
              placement="bottom"
            >
              <div class="health-item">
                <div class="health-title">
                  <span class="pet-name">{{ record.pet_name }}</span>
                  <span class="record-type">{{ record.record_type }}</span>
                </div>
                <div class="health-desc">{{ record.description }}</div>
              </div>
            </el-timeline-item>
          </el-timeline>
          <div v-else class="empty-reminder">
            <el-empty description="暂无健康记录" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, getUpcomingVaccinations, getRecentHealthRecords } from '@/api/statistics'
import { formatDate } from '@/utils/date'
import { House, Tools, FirstAidKit, Money } from '@element-plus/icons-vue'

const expenseChartRef = ref<HTMLElement>()
const expenseTypeChartRef = ref<HTMLElement>()
let expenseChart: echarts.ECharts | null = null
let expenseTypeChart: echarts.ECharts | null = null

const dashboardStats = ref<any>({})
const upcomingVaccinations = ref<any[]>([])
const recentHealthRecords = ref<any[]>([])

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    const [statsRes, vaccinesRes, healthRes] = await Promise.all([
      getDashboardStats(),
      getUpcomingVaccinations(30), // 获取30天内即将到期的疫苗
      getRecentHealthRecords(5) // 获取最近5条健康记录
    ])

    // 确保数据存在后再赋值
    if (statsRes?.data) {
      dashboardStats.value = statsRes.data
    }
    if (vaccinesRes?.data) {
      upcomingVaccinations.value = vaccinesRes.data
    }
    if (healthRes?.data) {
      recentHealthRecords.value = healthRes.data
    }

    // 只有在有数据时才初始化图表
    if (dashboardStats.value && Object.keys(dashboardStats.value).length > 0) {
      initCharts()
    }
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
    // 设置默认值防止页面崩溃
    dashboardStats.value = {}
  }
}

// 初始化图表
const initCharts = () => {
  if (expenseChartRef.value) {
    expenseChart = echarts.init(expenseChartRef.value)
    
    const expenseOption = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: dashboardStats.value.expense_trend_data?.months || ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '¥{value}'
        }
      },
      series: [
        {
          data: dashboardStats.value.expense_trend_data?.amounts || [0, 0, 0, 0, 0, 0],
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
    
    expenseChart.setOption(expenseOption)
  }
  
  if (expenseTypeChartRef.value) {
    expenseTypeChart = echarts.init(expenseTypeChartRef.value)
    
    const typeOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
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
          data: dashboardStats.value.expense_type_data?.map((item: any) => ({
            name: item.type_name,
            value: item.total_amount,
            itemStyle: {
              color: getTypeColor(item.type_name)
            }
          })) || []
        }
      ]
    }
    
    expenseTypeChart.setOption(typeOption)
  }
}

// 获取消费类型颜色
const getTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    '食品': '#409eff',
    '医疗': '#f56c6c',
    '美容': '#e6a23c',
    '疫苗': '#67c23a',
    '玩具': '#909399',
    '其他': '#9c27b0'
  }
  return colors[type] || '#409eff'
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  expenseChart?.resize()
  expenseTypeChart?.resize()
}

onMounted(() => {
  fetchDashboardData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  expenseChart?.dispose()
  expenseTypeChart?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.stat-info .stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-info .stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-info .stat-change {
  font-size: 12px;
  color: #909399;
}

.stat-change .increase {
  color: #67c23a;
  margin-right: 4px;
}

.stat-change .decrease {
  color: #f56c6c;
  margin-right: 4px;
}

.stat-change .warning {
  color: #e6a23c;
  margin-right: 4px;
}

.stat-change .normal {
  color: #67c23a;
  margin-right: 4px;
}

.stat-icon {
  opacity: 0.8;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 8px;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.reminder-row {
  margin-bottom: 20px;
}

.reminder-card {
  border-radius: 8px;
}

.reminder-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.reminder-item .pet-name {
  font-weight: 600;
  color: #333;
  margin-right: 8px;
}

.reminder-item .vaccine-name {
  color: #666;
}

.reminder-item .due-date {
  font-size: 12px;
  color: #e6a23c;
  margin-top: 2px;
}

.health-item {
  width: 100%;
}

.health-item .health-title {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.health-title .pet-name {
  font-weight: 600;
  color: #333;
}

.health-title .record-type {
  font-size: 12px;
  padding: 2px 8px;
  background: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
}

.health-item .health-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
  line-height: 1.4;
}

.health-item .health-date {
  font-size: 12px;
  color: #909399;
}

.empty-reminder {
  padding: 40px 0;
}
</style>
