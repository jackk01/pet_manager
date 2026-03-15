# 宠物信息管理系统

面向宠物主人的个人宠物信息管理系统，采用前后端分离架构，帮助用户系统化管理宠物的全生命周期信息。

## 功能特性

### 🐾 核心功能
- **用户管理**：用户注册、登录、个人信息管理、密码修改
- **宠物档案**：多宠物管理，支持基础信息录入、照片上传、档案编辑
- **疫苗管理**：疫苗记录录入，到期自动提醒，接种历史查询
- **健康管理**：就诊记录、体重追踪、驱虫记录、过敏管理、手术记录
- **消费管理**：日常开销记录，分类统计，消费趋势分析
- **数据统计**：多维度数据可视化，健康趋势、消费分析、仪表盘概览

### 🛡️ 安全特性
- JWT身份认证
- 用户数据隔离
- 密码加密存储
- 接口权限控制
- 输入参数校验

## 技术架构

### 后端技术栈
- **框架**: Django 5.0 + Django REST Framework
- **数据库**: MySQL 5.7+
- **认证**: JWT (djangorestframework-simplejwt)
- **部署**: Gunicorn + Nginx

### 前端技术栈
- **框架**: Vue 3.x + TypeScript
- **构建工具**: Vite
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **图表**: ECharts

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- MySQL 5.7+

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接信息

# 执行数据库迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务
npm run dev
```

前端服务启动后访问: http://localhost:5173

### 运行测试

```bash
cd backend

# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test users.tests
python manage.py test pets.tests
python manage.py test vaccinations.tests
python manage.py test health_records.tests
python manage.py test expenses.tests
```

## 项目结构

```
pet-manager/
├── backend/                 # 后端服务 (Django)
│   ├── pet_manager/        # 项目配置
│   ├── users/              # 用户模块
│   ├── pets/               # 宠物管理模块
│   ├── vaccinations/       # 疫苗管理模块
│   ├── health_records/     # 健康记录模块
│   ├── expenses/           # 消费管理模块
│   ├── statistics/         # 统计数据模块
│   ├── uploads/            # 文件上传目录
│   ├── .env.example        # 环境变量示例
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # 依赖列表
├── frontend/               # 前端应用 (Vue 3)
│   ├── src/
│   │   ├── api/            # API请求封装
│   │   ├── components/     # 公共组件
│   │   ├── stores/         # 状态管理
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   └── package.json
├── plans/                  # 项目文档
│   └── 需求文档.md
└── README.md               # 项目说明
```

## API接口

### 认证模块
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/refresh/` - 刷新令牌

### 用户模块
- `GET /api/user/profile/` - 获取用户信息
- `PUT /api/user/profile/` - 更新用户信息
- `PUT /api/user/password/` - 修改密码

### 宠物管理
- `GET /api/pets/` - 获取宠物列表
- `POST /api/pets/` - 添加宠物
- `GET /api/pets/{id}/` - 获取宠物详情
- `PUT /api/pets/{id}/` - 更新宠物信息
- `DELETE /api/pets/{id}/` - 删除宠物

### 疫苗管理
- `GET /api/vaccinations/` - 获取疫苗列表
- `POST /api/vaccinations/` - 添加疫苗记录
- `GET /api/vaccinations/{id}/` - 获取疫苗详情
- `PUT /api/vaccinations/{id}/` - 更新疫苗记录
- `DELETE /api/vaccinations/{id}/` - 删除疫苗记录

### 健康记录
- `GET /api/health-records/` - 获取健康记录列表
- `POST /api/health-records/` - 添加健康记录
- `GET /api/health-records/{id}/` - 获取健康记录详情
- `PUT /api/health-records/{id}/` - 更新健康记录
- `DELETE /api/health-records/{id}/` - 删除健康记录

### 消费管理
- `GET /api/expenses/` - 获取消费记录列表
- `POST /api/expenses/` - 添加消费记录
- `GET /api/expenses/{id}/` - 获取消费记录详情
- `PUT /api/expenses/{id}/` - 更新消费记录
- `DELETE /api/expenses/{id}/` - 删除消费记录

### 统计分析
- `GET /api/statistics/dashboard/` - 仪表盘数据
- `GET /api/statistics/upcoming-vaccinations/` - 即将到期疫苗
- `GET /api/statistics/recent-health-records/` - 最近健康记录
- `GET /api/statistics/expenses/` - 消费统计数据

## 环境变量配置

在 `backend/.env` 文件中配置以下内容：

```env
# Django配置
SECRET_KEY=your-secret-key-here
DEBUG=True
TZ=Asia/Shanghai

# 数据库配置
DB_NAME=pet_manager
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

## 部署说明

### 开发环境
1. 配置MySQL数据库，创建`pet_manager`数据库
2. 启动后端服务
3. 启动前端开发服务

### 生产环境
```bash
# 使用Gunicorn部署
cd backend
pip install gunicorn
gunicorn pet_manager.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 开发规范

### 后端规范
- 遵循PEP8编码规范
- 使用类型注解
- 接口遵循RESTful设计规范
- 数据库操作使用ORM

### 前端规范
- 使用TypeScript类型注解
- 遵循Vue 3 Composition API规范
- 组件化开发，提高代码复用性
- 响应式设计，支持PC和移动端

## 许可证
MIT License