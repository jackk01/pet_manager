export interface PetDto {
    id: number
    name: string
    breed?: string
    gender?: '公' | '母' | '未知'
    birth_date?: string
    weight?: number
    color?: string
    chip_number?: string
    description?: string
    personality?: string
    avatar?: string
    is_active?: boolean
    created_at: string
    updated_at: string
    vaccination_count?: number
    health_record_count?: number
    total_expense?: number
}

export interface CreatePetDto {
    name: string
    breed?: string
    gender?: string
    birth_date?: string
    weight?: number
    color?: string
    chip_number?: string
    description?: string
    personality?: string
    avatar?: string
}

export interface UpdatePetDto {
    name?: string
    breed?: string
    gender?: string
    birth_date?: string
    weight?: number
    color?: string
    chip_number?: string
    description?: string
    personality?: string
    avatar?: string
    is_active?: boolean
}
