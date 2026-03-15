// 格式化日期
export function formatDate(date: string | Date, format: string = 'YYYY-MM-DD'): string {
    if (!date) return ''
    const d = new Date(date)
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hour = String(d.getHours()).padStart(2, '0')
    const minute = String(d.getMinutes()).padStart(2, '0')
    const second = String(d.getSeconds()).padStart(2, '0')

    return format
        .replace('YYYY', String(year))
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hour)
        .replace('mm', minute)
        .replace('ss', second)
}

// 格式化日期时间
export function formatDateTime(date: string | Date): string {
    return formatDate(date, 'YYYY-MM-DD HH:mm:ss')
}

// 计算两个日期之间的天数
export function daysBetween(date1: string | Date, date2: string | Date): number {
    const oneDay = 24 * 60 * 60 * 1000
    const d1 = new Date(date1)
    const d2 = new Date(date2)
    return Math.round(Math.abs((d1.getTime() - d2.getTime()) / oneDay))
}

// 判断日期是否已过期
export function isExpired(date: string | Date): boolean {
    return new Date(date) < new Date()
}

// 判断日期是否即将到期（days天内）
export function isUpcoming(date: string | Date, days: number = 7): boolean {
    const now = new Date()
    const target = new Date(date)
    const diff = target.getTime() - now.getTime()
    return diff > 0 && diff <= days * 24 * 60 * 60 * 1000
}
