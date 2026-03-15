from datetime import date, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_pet import pet as crud_pet
from app.crud.crud_vaccination import vaccination as crud_vaccination
from app.crud.crud_health_record import health_record as crud_health_record
from app.crud.crud_expense import expense as crud_expense
from app.db.session import get_db
from app.models.user import User
from app.models.pet import Pet

router = APIRouter()


@router.get("/dashboard", summary="获取仪表盘统计数据")
def get_dashboard_statistics(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户的仪表盘统计数据
    """
    # 宠物数量
    pet_count = crud_pet.count_by_user_id(db, user_id=current_user.id)
    
    # 即将到期的疫苗提醒数量
    upcoming_vaccinations = crud_vaccination.get_upcoming_by_user_id(
        db, user_id=current_user.id, days=30
    )
    upcoming_vaccination_count = len(upcoming_vaccinations)
    
    # 已过期的疫苗数量
    expired_vaccinations = crud_vaccination.get_expired_by_user_id(
        db, user_id=current_user.id
    )
    expired_vaccination_count = len(expired_vaccinations)
    
    # 即将到来的复查提醒数量
    upcoming_checkups = crud_health_record.get_upcoming_checkups(
        db, user_id=current_user.id, days=30
    )
    upcoming_checkup_count = len(upcoming_checkups)
    
    # 本月消费总额
    today = date.today()
    month_start = date(today.year, today.month, 1)
    month_end = date(today.year, today.month + 1, 1) if today.month < 12 else date(today.year + 1, 1, 1)
    
    monthly_expense = crud_expense.get_total_amount_by_user_id(
        db,
        user_id=current_user.id,
        start_date=month_start,
        end_date=month_end
    )
    
    # 年度消费总额
    year_start = date(today.year, 1, 1)
    year_end = date(today.year + 1, 1, 1)
    
    yearly_expense = crud_expense.get_total_amount_by_user_id(
        db,
        user_id=current_user.id,
        start_date=year_start,
        end_date=year_end
    )
    
    # 获取近6个月消费数据
    expense_trend_data = {"months": [], "amounts": []}
    for i in range(5, -1, -1):
        month_date = date(today.year, today.month, 1) - timedelta(days=i*30)
        month_start = date(month_date.year, month_date.month, 1)
        if month_date.month == 12:
            month_end = date(month_date.year + 1, 1, 1)
        else:
            month_end = date(month_date.year, month_date.month + 1, 1)
        
        month_expense = crud_expense.get_total_amount_by_user_id(
            db,
            user_id=current_user.id,
            start_date=month_start,
            end_date=month_end
        )
        expense_trend_data["months"].append(f"{month_date.month}月")
        expense_trend_data["amounts"].append(month_expense)
    
    # 获取消费类型分布
    expense_type_data = crud_expense.get_statistics_by_user_id(
        db, user_id=current_user.id, year=today.year
    ).get("category_stats", [])
    
    # 计算月度健康记录数
    monthly_health_records = db.query(func.count(crud_health_record.model.id))\
        .join(Pet, crud_health_record.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == current_user.id,
            crud_health_record.model.record_date >= month_start,
            crud_health_record.model.record_date < month_end
        ).scalar() or 0
    
    # 计算上月消费用于趋势
    last_month_start = date(today.year, today.month - 1, 1) if today.month > 1 else date(today.year - 1, 12, 1)
    last_month_end = month_start
    last_month_expense = crud_expense.get_total_amount_by_user_id(
        db,
        user_id=current_user.id,
        start_date=last_month_start,
        end_date=last_month_end
    )
    expense_trend = round((monthly_expense - last_month_expense) / last_month_expense * 100, 1) if last_month_expense > 0 else 0
    
    # 健康记录总数
    health_record_count = db.query(func.count(crud_health_record.model.id))\
        .join(Pet, crud_health_record.model.pet_id == Pet.id)\
        .filter(Pet.user_id == current_user.id).scalar() or 0
    
    return {
        "pet_count": pet_count,
        "upcoming_vaccinations_count": upcoming_vaccination_count,
        "expired_vaccination_count": expired_vaccination_count,
        "upcoming_checkup_count": upcoming_checkup_count,
        "monthly_total_expense": monthly_expense,
        "yearly_expense": yearly_expense,
        "monthly_health_records": monthly_health_records,
        "health_record_count": health_record_count,
        "expense_trend": expense_trend,
        "expense_trend_data": expense_trend_data,
        "expense_type_data": expense_type_data,
        "current_month": f"{today.year}年{today.month}月",
        "current_year": f"{today.year}年"
    }


@router.get("/overview", summary="获取用户整体数据概览")
def get_overview_statistics(
    *,
    db: Session = Depends(get_db),
    year: Optional[int] = Query(None, description="统计年份，默认当前年"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户的整体数据概览
    """
    if not year:
        year = date.today().year
    
    # 消费统计
    expense_stats = crud_expense.get_statistics_by_user_id(
        db, user_id=current_user.id, year=year
    )
    
    # 疫苗统计
    from app.models.pet import Pet
    
    vaccination_count = db.query(func.count(crud_vaccination.model.id))\
        .join(Pet, crud_vaccination.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == current_user.id,
            Pet.is_active == True,
            func.year(crud_vaccination.model.vaccination_date) == year
        ).scalar() or 0
    
    # 健康记录统计
    health_record_count = db.query(func.count(crud_health_record.model.id))\
        .join(Pet, crud_health_record.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == current_user.id,
            Pet.is_active == True,
            func.year(crud_health_record.model.record_date) == year
        ).scalar() or 0
    
    return {
        "year": year,
        "total_expense": expense_stats.get("total_amount", 0),
        "expense_category_stats": expense_stats.get("category_stats", {}),
        "expense_month_stats": expense_stats.get("month_stats", {}),
        "expense_pet_stats": expense_stats.get("pet_stats", {}),
        "vaccination_count": vaccination_count,
        "health_record_count": health_record_count
    }


@router.get("/pets/{pet_id}", summary="获取指定宠物的综合统计数据")
def get_pet_statistics(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    year: Optional[int] = Query(None, description="统计年份，默认当前年"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的综合统计数据
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    if not year:
        year = date.today().year
    
    # 疫苗统计
    vaccination_count = crud_vaccination.count_by_pet_id(db, pet_id=pet_id)
    upcoming_vaccinations = crud_vaccination.get_upcoming_by_user_id(
        db, user_id=current_user.id, days=30
    )
    upcoming_vaccination_count = len([v for v in upcoming_vaccinations if v.pet_id == pet_id])
    
    # 健康记录统计
    health_record_count = crud_health_record.count_by_pet_id(db, pet_id=pet_id)
    upcoming_checkups = crud_health_record.get_upcoming_checkups(
        db, user_id=current_user.id, days=30
    )
    upcoming_checkup_count = len([c for c in upcoming_checkups if c.pet_id == pet_id])
    
    # 消费统计
    expense_stats = crud_expense.get_statistics_by_pet_id(
        db, pet_id=pet_id, year=year
    )
    
    # 体重趋势
    weight_trend = crud_health_record.get_weight_trend(db, pet_id=pet_id)
    
    return {
        "pet_id": pet_id,
        "pet_name": pet.name,
        "year": year,
        "vaccination_count": vaccination_count,
        "upcoming_vaccination_count": upcoming_vaccination_count,
        "health_record_count": health_record_count,
        "upcoming_checkup_count": upcoming_checkup_count,
        "total_expense": expense_stats.get("total_amount", 0),
        "expense_category_stats": expense_stats.get("category_stats", {}),
        "expense_month_stats": expense_stats.get("month_stats", {}),
        "weight_trend": [
            {"date": d.isoformat(), "weight": w}
            for d, w in weight_trend
        ]
    }


@router.get("/upcoming-vaccinations/", summary="获取即将到期的疫苗")
def get_upcoming_vaccinations(
    *,
    days: int = Query(30, description="查询天数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户宠物的即将到期的疫苗列表
    """
    vaccinations = crud_vaccination.get_upcoming_by_user_id(
        db, user_id=current_user.id, days=days
    )
    
    # 构建返回数据
    result = []
    for v in vaccinations:
        pet = db.query(crud_pet.model).filter(crud_pet.model.id == v.pet_id).first()
        result.append({
            "id": v.id,
            "pet_id": v.pet_id,
            "pet_name": pet.name if pet else "未知",
            "vaccine_name": v.vaccine_name,
            "due_date": v.due_date.isoformat() if v.due_date else None,
            "vaccination_date": v.vaccination_date.isoformat() if v.vaccination_date else None,
            "notes": v.notes
        })
    
    return result


@router.get("/recent-health-records/", summary="获取最近的健康记录")
def get_recent_health_records(
    *,
    limit: int = Query(5, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户宠物的最近健康记录
    """
    from app.models.pet import Pet
    
    # 查询当前用户宠物的健康记录
    records = db.query(crud_health_record.model)\
        .join(Pet, crud_health_record.model.pet_id == Pet.id)\
        .filter(Pet.user_id == current_user.id)\
        .order_by(crud_health_record.model.record_date.desc())\
        .limit(limit)\
        .all()
    
    # 构建返回数据
    result = []
    for r in records:
        pet = db.query(crud_pet.model).filter(crud_pet.model.id == r.pet_id).first()
        result.append({
            "id": r.id,
            "pet_id": r.pet_id,
            "pet_name": pet.name if pet else "未知",
            "record_type": r.record_type,
            "description": r.description,
            "visit_date": r.record_date.isoformat() if r.record_date else None,
            "next_visit_date": r.next_visit_date.isoformat() if r.next_visit_date else None,
            "weight": r.weight,
            "notes": r.notes
        })
    
    return result
