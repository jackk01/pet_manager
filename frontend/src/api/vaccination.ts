import request from '@/utils/request'
import type { VaccinationDto, CreateVaccinationDto, UpdateVaccinationDto } from '@/types/vaccination'

// 获取疫苗记录列表
export function getVaccinationList(params?: any) {
    return request<{ data: { items: VaccinationDto[]; total: number } }>({
        url: '/vaccinations',
        method: 'get',
        params
    })
}

// 获取疫苗记录详情
export function getVaccinationDetail(id: number) {
    return request<{ data: VaccinationDto }>({
        url: `/vaccinations/${id}`,
        method: 'get'
    })
}

// 创建疫苗记录
export function createVaccination(data: CreateVaccinationDto) {
    return request({
        url: '/vaccinations',
        method: 'post',
        data
    })
}

// 更新疫苗记录
export function updateVaccination(id: number, data: UpdateVaccinationDto) {
    return request({
        url: `/vaccinations/${id}`,
        method: 'put',
        data
    })
}

// 删除疫苗记录
export function deleteVaccination(id: number) {
    return request({
        url: `/vaccinations/${id}`,
        method: 'delete'
    })
}