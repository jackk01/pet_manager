export interface VaccinationDto {
    id: number
    pet_id: number
    pet_name?: string
    pet_avatar?: string
    vaccine_name: string
    vaccination_date: string
    next_due_date?: string
    clinic?: string
    doctor?: string
    batch_number?: string
    remark?: string
    attachment?: string
    is_reminded?: boolean
    created_at: string
    updated_at: string
}

export interface CreateVaccinationDto {
    pet_id: number
    vaccine_name: string
    vaccination_date: string
    next_due_date?: string
    clinic?: string
    doctor?: string
    batch_number?: string
    remark?: string
    attachment?: string
}

export interface UpdateVaccinationDto {
    pet_id?: number
    vaccine_name?: string
    vaccination_date?: string
    next_due_date?: string
    clinic?: string
    doctor?: string
    batch_number?: string
    remark?: string
    attachment?: string
}
