import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '@/types/user'
import { getUserInfo as getUserInfoApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
    const token = ref<string | null>(localStorage.getItem('token'))
    const userInfo = ref<UserInfo | null>(null)

    const setToken = (val: string) => {
        token.value = val
        localStorage.setItem('token', val)
    }

    const setUserInfo = (val: UserInfo) => {
        userInfo.value = val
        localStorage.setItem('userInfo', JSON.stringify(val))
    }

    const logout = () => {
        token.value = null
        userInfo.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
    }

    // 获取用户信息
    const getUserInfo = async () => {
        try {
            const res = await getUserInfoApi()
            setUserInfo(res as unknown as UserInfo)
            return res
        } catch (error) {
            console.error('获取用户信息失败:', error)
            throw error
        }
    }

    // 初始化时从localStorage读取用户信息
    const initUserInfo = () => {
        const userInfoStr = localStorage.getItem('userInfo')
        if (userInfoStr) {
            try {
                userInfo.value = JSON.parse(userInfoStr)
            } catch (e) {
                console.error('解析用户信息失败:', e)
                logout()
            }
        }
    }

    initUserInfo()

    return {
        token,
        userInfo,
        setToken,
        setUserInfo,
        logout,
        getUserInfo
    }
})
