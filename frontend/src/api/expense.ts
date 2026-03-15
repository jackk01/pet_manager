import request from '@/utils/request'
import type { ExpenseDto, CreateExpenseDto, UpdateExpenseDto } from '@/types/expense'

// 获取消费记录列表
export function getExpenseList(params?: any) {
    return request<{ data: { items: ExpenseDto[]; total: number } }>({
        url: '/expenses',
        method: 'get',
        params
    })
}

// 获取消费记录详情
export function getExpenseDetail(id: number) {
    return request<{ data: ExpenseDto }>({
        url: `/expenses/${id}`,
        method: 'get'
    })
}

// 创建消费记录
export function createExpense(data: CreateExpenseDto) {
    return request({
        url: '/expenses',
        method: 'post',
        data
    })
}

// 更新消费记录
export function updateExpense(id: number, data: UpdateExpenseDto) {
    return request({
        url: `/expenses/${id}`,
        method: 'put',
        data
    })
}

// 删除消费记录
export function deleteExpense(id: number) {
    return request({
        url: `/expenses/${id}`,
        method: 'delete'
    })
}

// 获取消费统计
export function getExpenseStats() {
    return request<{ data: any }>({
        url: '/expenses/stats',
        method: 'get'
    })
}