#!/bin/bash

# ==================== 后端启动 ====================
cd /Users/longyang/Desktop/code/demo/backend

# 1. 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 创建数据库（需要先配置 MySQL）
# mysql -u root -p123456 -e "CREATE DATABASE pet_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 5. 执行数据库迁移
python manage.py migrate

# 6. 创建超级用户（可选）
# python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver 0.0.0.0:8000

# ==================== 前端启动 ====================
# 打开新终端窗口
cd /Users/longyang/Desktop/code/demo/frontend
npm install
# 或
# pnpm install
npm run dev

# ==================== 单元测试 ====================
# 运行所有测试
cd /Users/longyang/Desktop/code/demo/backend
python manage.py test

# 运行特定应用的测试
python manage.py test users.tests
python manage.py test pets.tests
python manage.py test vaccinations.tests
python manage.py test health_records.tests
python manage.py test expenses.tests
python manage.py test expenses.tests.test_models

# 生成测试覆盖率报告（需要安装 coverage）
# pip install coverage
# coverage run manage.py test
# coverage report