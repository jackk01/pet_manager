import request from '@/utils/request'
import type { UpdateUserProfileDto, ChangePasswordDto, UpdateUserSettingsDto } from '@/types/user'

// 获取用户信息
export function getUserInfo() {
    return request({
        url: '/user/profile',
        method: 'get'
    })
}

// 更新用户信息
export function updateUserProfile(data: UpdateUserProfileDto) {
    return request({
        url: '/user/profile',
        method: 'put',
        data
    })
}

// 修改密码
export function changePassword(data: ChangePasswordDto) {
    return request({
        url: '/user/password',
        method: 'put',
        data
    })
}

// 获取用户统计数据
export function getUserStats() {
    return request({
        url: '/user/stats',
        method: 'get'
    })
}

// 更新用户设置
export function updateUserSettings(data: UpdateUserSettingsDto) {
    return request({
        url: '/user/settings',
        method: 'put',
        data
    })
}