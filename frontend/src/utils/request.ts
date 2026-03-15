import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const service: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    }
})

// 请求拦截器
service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('token')
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        console.error('Request error:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    (response: AxiosResponse) => {
        const res = response.data
        return res
    },
    (error) => {
        console.error('Response error:', error)

        if (error.response) {
            const { status, data } = error.response

            switch (status) {
                case 400:
                    ElMessage.error(data.message || '请求参数错误')
                    break
                case 401:
                    ElMessageBox.confirm(
                        '登录状态已过期，请重新登录',
                        '系统提示',
                        {
                            confirmButtonText: '重新登录',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }
                    ).then(() => {
                        localStorage.removeItem('token')
                        localStorage.removeItem('userInfo')
                        location.href = '/login'
                    })
                    break
                case 403:
                    ElMessage.error('没有权限访问该资源')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 500:
                    ElMessage.error(data.message || '服务器内部错误')
                    break
                default:
                    ElMessage.error(`请求错误: ${status}`)
            }
        } else {
            ElMessage.error('网络连接异常，请检查网络设置')
        }

        return Promise.reject(error)
    }
)

export default service
