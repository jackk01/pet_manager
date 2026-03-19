import request from '@/utils/request'
import type { NotificationDto } from '@/types/notification'

export function getNotifications(params?: { page?: number; size?: number; unread_only?: boolean; days?: number }) {
  return request<{ items: NotificationDto[]; total: number; unread_count: number }>({
    url: '/notifications',
    method: 'get',
    params
  })
}

export function getNotificationUnreadCount(days: number = 14) {
  return request<{ unread_count: number }>({
    url: '/notifications/unread-count',
    method: 'get',
    params: { days }
  })
}

export function markNotificationsRead(data: { ids?: number[]; read_all?: boolean }) {
  return request<{ updated: number; unread_count: number }>({
    url: '/notifications/mark-read',
    method: 'post',
    data
  })
}
