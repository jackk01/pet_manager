import request from '@/utils/request'
import type { HealthRecordDto, CreateHealthRecordDto, UpdateHealthRecordDto } from '@/types/health'

// 获取健康记录列表
export function getHealthRecordList(params?: any) {
    return request<{ data: { items: HealthRecordDto[]; total: number } }>({
        url: '/health-records',
        method: 'get',
        params
    })
}

// 获取健康记录详情
export function getHealthRecordDetail(id: number) {
    return request<{ data: HealthRecordDto }>({
        url: `/health-records/${id}`,
        method: 'get'
    })
}

// 创建健康记录
export function createHealthRecord(data: CreateHealthRecordDto) {
    return request({
        url: '/health-records',
        method: 'post',
        data
    })
}

// 更新健康记录
export function updateHealthRecord(id: number, data: UpdateHealthRecordDto) {
    return request({
        url: `/health-records/${id}`,
        method: 'put',
        data
    })
}

// 删除健康记录
export function deleteHealthRecord(id: number) {
    return request({
        url: `/health-records/${id}`,
        method: 'delete'
    })
}