export interface HealthRecordDto {
    id: number
    pet_id: number
    pet_name?: string
    pet_avatar?: string
    record_type: '就诊' | '体检' | '体重' | '驱虫' | '过敏' | '手术' | '其他'
    record_date: string
    title: string
    content?: string
    hospital?: string
    doctor?: string
    cost?: number
    attachment?: string
    next_check_date?: string
    created_at: string
    updated_at: string
}

export interface CreateHealthRecordDto {
    pet_id: number
    record_type: string
    record_date: string
    title: string
    content?: string
    hospital?: string
    doctor?: string
    cost?: number
    attachment?: string
    next_check_date?: string
}

export interface UpdateHealthRecordDto {
    pet_id?: number
    record_type?: string
    record_date?: string
    title?: string
    content?: string
    hospital?: string
    doctor?: number
    cost?: number
    attachment?: string
    next_check_date?: string
}
