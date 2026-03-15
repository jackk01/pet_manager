export interface ExpenseDto {
    id: number
    pet_id: number
    pet_name?: string
    pet_avatar?: string
    category: 'food' | 'medical' | 'grooming' | 'supplies' | 'insurance' | 'other'
    expense_date: string
    amount: number
    merchant?: string
    remark?: string
    attachment?: string
    created_at: string
    updated_at: string
}

export interface CreateExpenseDto {
    pet_id: number
    category: string
    expense_date: string
    amount: number
    merchant?: string
    remark?: string
    attachment?: string
}

export interface UpdateExpenseDto {
    pet_id?: number
    category?: string
    expense_date?: string
    amount?: number
    merchant?: string
    remark?: string
    attachment?: string
}
