import request from '@/utils/request'

// 获取仪表盘统计数据
export function getDashboardStats() {
    return request({
        url: '/statistics/dashboard',
        method: 'get'
    })
}

// 获取即将到期的疫苗
export function getUpcomingVaccinations(days: number = 30) {
    return request({
        url: '/statistics/upcoming-vaccinations',
        method: 'get',
        params: { days }
    })
}

// 获取最近的健康记录
export function getRecentHealthRecords(limit: number = 5) {
    return request({
        url: '/statistics/recent-health-records',
        method: 'get',
        params: { limit }
    })
}

// 获取完整统计数据
export function getStatistics(params?: any) {
    return request({
        url: '/statistics',
        method: 'get',
        params
    })
}