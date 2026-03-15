import request from '@/utils/request'
import type { PetDto, CreatePetDto, UpdatePetDto } from '@/types/pet'

// 获取宠物列表
export function getPetList() {
    return request<{ data: PetDto[] }>({
        url: '/pets',
        method: 'get'
    })
}

// 获取宠物详情
export function getPetDetail(id: number) {
    return request<{ data: PetDto }>({
        url: `/pets/${id}`,
        method: 'get'
    })
}

// 创建宠物
export function createPet(data: CreatePetDto) {
    return request({
        url: '/pets',
        method: 'post',
        data
    })
}

// 更新宠物
export function updatePet(id: number, data: UpdatePetDto) {
    return request({
        url: `/pets/${id}`,
        method: 'put',
        data
    })
}

// 删除宠物
export function deletePet(id: number) {
    return request({
        url: `/pets/${id}`,
        method: 'delete'
    })
}
