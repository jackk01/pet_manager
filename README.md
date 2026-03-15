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
- **框架**: FastAPI 0.104.1 (Python 3.10+)
- **数据库**: MySQL 5.7 + Redis 6.x
- **ORM**: SQLAlchemy 2.0 + Alembic
- **认证**: JWT + Passlib
- **任务队列**: Celery (定时提醒)
- **部署**: Docker + Nginx

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
- MySQL 5.7
- Redis 6.x+

### 后端启动
```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接信息

# 启动服务
python app/main.py
uvicorn app.main:app --reload --port 8000
```
后端服务启动后访问: http://localhost:8000/docs 查看API文档

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

### 默认测试账号
- 用户名: `admin`
- 密码: `123456`

## 项目结构

```
pet-manager/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API接口层
│   │   ├── core/           # 核心配置
│   │   ├── crud/           # 数据操作层
│   │   ├── db/             # 数据库相关
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   └── main.py         # 项目入口
│   ├── uploads/            # 文件上传目录
│   ├── .env.example        # 环境变量示例
│   └── requirements.txt    # 依赖列表
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/            # API请求封装
│   │   ├── components/     # 公共组件
│   │   ├── stores/         # 状态管理
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   └── package.json
├── plans/                  # 项目文档
│   ├── 需求文档.md
│   └── 技术方案.md
└── README.md               # 项目说明
```

## API接口

### 认证模块
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh-token` - 刷新令牌

### 用户模块
- `GET /api/user/profile` - 获取用户信息
- `PUT /api/user/profile` - 更新用户信息
- `PUT /api/user/password` - 修改密码

### 宠物管理
- `GET /api/pets` - 获取宠物列表
- `POST /api/pets` - 添加宠物
- `GET /api/pets/{id}` - 获取宠物详情
- `PUT /api/pets/{id}` - 更新宠物信息
- `DELETE /api/pets/{id}` - 删除宠物

### 疫苗管理
- `GET /api/vaccinations/upcoming` - 即将到期的疫苗提醒
- `GET /api/vaccinations/pets/{pet_id}` - 获取宠物疫苗记录
- `POST /api/vaccinations/pets/{pet_id}` - 添加疫苗记录

### 健康记录
- `GET /api/health-records/pets/{pet_id}` - 获取健康记录
- `POST /api/health-records/pets/{pet_id}` - 添加健康记录
- `GET /api/health-records/pets/{pet_id}/weight-trend` - 体重变化趋势

### 消费管理
- `GET /api/expenses` - 获取所有消费记录
- `GET /api/expenses/pets/{pet_id}` - 获取宠物消费记录
- `POST /api/expenses/pets/{pet_id}` - 添加消费记录
- `GET /api/expenses/statistics` - 消费统计数据

### 统计分析
- `GET /api/statistics/dashboard` - 仪表盘数据
- `GET /api/statistics/overview` - 整体数据概览
- `GET /api/statistics/pets/{pet_id}` - 宠物综合统计

## 部署说明

### 开发环境
1. 配置MySQL数据库，创建`pet_manager`数据库
2. 配置Redis服务
3. 启动后端服务
4. 启动前端开发服务

### 生产环境
推荐使用Docker Compose一键部署：
```bash
docker-compose up -d
```

详细部署说明请参考 [部署文档](./docs/DEPLOY.md)

## 开发规范

### 后端规范
- 遵循PEP8编码规范
- 使用类型注解
- 接口遵循RESTful设计规范
- 数据库操作使用ORM，禁止直接拼接SQL

### 前端规范
- 使用TypeScript类型注解
- 遵循Vue 3 Composition API规范
- 组件化开发，提高代码复用性
- 响应式设计，支持PC和移动端

## 功能规划

### 二期功能
- [ ] 数据导出功能（PDF/Excel）
- [ ] PWA支持，离线访问
- [ ] 邮件/短信提醒
- [ ] 数据备份与恢复
- [ ] 移动端适配优化

### 三期功能
- [ ] 社区交流功能
- [ ] 宠物匹配功能
- [ ] 第三方服务集成
- [ ] 多用户数据共享

## 许可证
MIT License
