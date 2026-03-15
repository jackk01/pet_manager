# 宠物信息管理系统 - 后端

## 技术栈
- Python 3.10+
- FastAPI 0.104.1
- SQLAlchemy 2.0
- MySQL 8.0+
- Redis 6.x+
- Celery 5.3+

## 快速开始

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
# 复制环境变量配置文件
cp .env.example .env

# 修改 .env 文件中的配置信息，特别是数据库连接信息
```

### 3. 数据库初始化
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE pet_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 初始化表结构（开发环境）
# 首次运行时会自动创建表结构
```

### 4. 启动服务
```bash
# 开发环境启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行主文件
python app/main.py
```

### 5. 访问接口文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构
```
backend/
├── app/
│   ├── api/                    # API接口层
│   │   ├── api_v1/            # v1版本API
│   │   │   ├── endpoints/     # 接口端点
│   │   │   └── api.py         # API路由注册
│   │   └── deps.py            # 依赖注入
│   ├── core/                   # 核心配置
│   │   ├── config.py          # 配置文件
│   │   ├── security.py        # 安全相关
│   │   └── celery.py          # 任务队列配置
│   ├── crud/                   # CRUD操作层
│   ├── db/                     # 数据库相关
│   │   ├── base.py            # 模型基类
│   │   └── session.py         # 数据库会话
│   ├── models/                 # 数据模型层
│   ├── schemas/                # Pydantic模型层
│   ├── utils/                  # 工具类
│   └── main.py                # 项目入口
├── uploads/                    # 文件上传目录
├── .env.example               # 环境变量示例
├── requirements.txt           # 依赖包列表
└── README.md                  # 项目说明
```

## 主要功能模块
- [x] 用户认证与授权
- [x] 用户信息管理
- [ ] 宠物档案管理
- [ ] 疫苗记录与提醒
- [ ] 健康记录管理
- [ ] 消费记录管理
- [ ] 数据统计与可视化
- [ ] 文件上传与下载
- [ ] 数据导出功能

## 开发规范
- 遵循 PEP8 编码规范
- 使用类型注解
- 接口遵循 RESTful 设计规范
- 数据库操作使用 ORM，禁止直接拼接 SQL
- 错误信息使用统一格式返回

## 部署说明
### 生产环境部署
```bash
# 使用 Gunicorn + Uvicorn 部署
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 启动 Celery  worker
celery -A app.core.celery worker --loglevel=info

# 启动定时任务
celery -A app.core.celery beat --loglevel=info
```

### Docker 部署
```bash
# 构建镜像
docker build -t pet-manager-backend .

# 运行容器
docker run -d -p 8000:8000 --name pet-manager-backend pet-manager-backend
```
