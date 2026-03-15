import request from '@/utils/request'
import type { LoginForm, RegisterForm, LoginResponse, UserInfo } from '@/types/user'

/**
 * 用户登录
 */
export function login(data: LoginForm) {
    return request<LoginResponse>({
        url: '/auth/login',
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: new URLSearchParams({
            username: data.username,
            password: data.password
        })
    })
}

/**
 * 用户注册
 */
export function register(data: RegisterForm) {
    return request<UserInfo>({
        url: '/auth/register',
        method: 'post',
        data
    })
}

/**
 * 刷新令牌
 */
export function refreshToken(refreshToken: string) {
    return request<LoginResponse>({
        url: '/auth/refresh-token',
        method: 'post',
        data: {
            refresh: refreshToken
        }
    })
}

/**
 * 获取当前用户信息
 */
export function getUserInfo() {
    return request<UserInfo>({
        url: '/user/profile',
        method: 'get'
    })
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data: Partial<UserInfo>) {
    return request<UserInfo>({
        url: '/user/profile',
        method: 'put',
        data
    })
}

/**
 * 修改密码
 */
export function changePassword(data: { old_password: string; new_password: string }) {
    return request({
        url: '/user/password',
        method: 'put',
        data
    })
}