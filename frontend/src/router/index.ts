import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/login/Login.vue'),
        meta: {
            requiresAuth: false,
            title: '登录'
        }
    },
    {
        path: '/',
        component: () => import('@/components/layout/Layout.vue'),
        redirect: '/dashboard',
        meta: {
            requiresAuth: true
        },
        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('@/views/dashboard/Dashboard.vue'),
                meta: {
                    title: '仪表盘',
                    icon: 'Odometer'
                }
            },
            {
                path: 'pets',
                name: 'Pets',
                component: () => import('@/views/pet/PetList.vue'),
                meta: {
                    title: '宠物管理',
                    icon: 'Dog'
                }
            },
            {
                path: 'vaccinations',
                name: 'Vaccinations',
                component: () => import('@/views/vaccination/VaccinationList.vue'),
                meta: {
                    title: '疫苗管理',
                    icon: 'Syringe'
                }
            },
            {
                path: 'health',
                name: 'Health',
                component: () => import('@/views/health/HealthList.vue'),
                meta: {
                    title: '健康管理',
                    icon: 'Medical'
                }
            },
            {
                path: 'expenses',
                name: 'Expenses',
                component: () => import('@/views/expense/ExpenseList.vue'),
                meta: {
                    title: '消费管理',
                    icon: 'Money'
                }
            },
            {
                path: 'statistics',
                name: 'Statistics',
                component: () => import('@/views/statistics/Statistics.vue'),
                meta: {
                    title: '数据统计',
                    icon: 'DataAnalysis'
                }
            },
            {
                path: 'profile',
                name: 'Profile',
                component: () => import('@/views/user/Profile.vue'),
                meta: {
                    title: '个人中心',
                    icon: 'User'
                }
            }
        ]
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/error/404.vue'),
        meta: {
            title: '页面不存在'
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    const token = userStore.token

    // 设置页面标题
    if (to.meta.title) {
        document.title = `${to.meta.title} - 宠物信息管理系统`
    }

    // 需要登录的页面
    if (to.meta.requiresAuth) {
        if (!token) {
            next({ name: 'Login', query: { redirect: to.fullPath } })
        } else {
            next()
        }
    } else {
        // 登录页和注册页，已登录用户跳转到首页
        if ((to.name === 'Login' || to.name === 'Register') && token) {
            next({ name: 'Dashboard' })
        } else {
            next()
        }
    }
})

export default router
