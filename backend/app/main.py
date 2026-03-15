from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import engine

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url=f"{settings.API_PREFIX}/openapi.json" if settings.DEBUG else None
)

# 配置CORS - 默认允许所有开发环境请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册API路由
app.include_router(api_router, prefix=settings.API_PREFIX)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    """
    应用启动时执行的操作
    """
    # 初始化数据库表（生产环境建议使用alembic迁移）
    if settings.DEBUG:
        from app.db.base import Base
        Base.metadata.create_all(bind=engine)
    
    # 初始化基础数据
    init_db()

@app.get("/")
async def root():
    """
    根路径访问
    """
    return {
        "message": f"欢迎使用{settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation is disabled in production"
    }

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
