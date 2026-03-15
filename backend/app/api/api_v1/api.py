from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, user, pet, vaccination, health_record, expense, statistics

api_router = APIRouter()

# 认证相关接口
api_router.include_router(auth.router, prefix="/auth", tags=["认证管理"])

# 用户相关接口
api_router.include_router(user.router, prefix="/user", tags=["用户管理"])

# 宠物相关接口
api_router.include_router(pet.router, prefix="/pets", tags=["宠物管理"])

# 疫苗相关接口
api_router.include_router(vaccination.router, prefix="/vaccinations", tags=["疫苗管理"])

# 健康记录相关接口
api_router.include_router(health_record.router, prefix="/health-records", tags=["健康记录管理"])

# 消费相关接口
api_router.include_router(expense.router, prefix="/expenses", tags=["消费管理"])

# 统计相关接口
api_router.include_router(statistics.router, prefix="/statistics", tags=["统计分析"])

# 通用接口
# api_router.include_router(common.router, prefix="/common", tags=["通用功能"])
