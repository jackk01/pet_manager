export interface UserInfo {
    id: number
    username: string
    email: string
    nickname: string
    avatar?: string
    phone?: string
    is_active: boolean
    created_at: string
    updated_at: string
}

export interface LoginForm {
    username: string
    password: string
}

export interface RegisterForm {
    username: string
    email: string
    password: string
    nickname?: string
    phone?: string
}

export interface LoginResponse {
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
}

export interface UpdateUserProfileDto {
    username?: string
    email?: string
    full_name?: string
    phone?: string
    birth_date?: string
    gender?: 'male' | 'female' | 'unknown'
    address?: string
}

export interface ChangePasswordDto {
    old_password: string
    new_password: string
}

export interface UpdateUserSettingsDto {
    email_notification?: boolean
    sms_notification?: boolean
    remind_days?: number
    language?: string
    theme?: string
}
