export interface NotificationDto {
  id: number
  message_type: 'vaccination' | 'deworming'
  message_type_display: string
  title: string
  content: string
  pet_name?: string
  due_date?: string
  days_left?: number | null
  is_read: boolean
  created_at: string
  updated_at: string
}
