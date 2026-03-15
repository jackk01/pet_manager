cd /Users/longyang/Desktop/code/demo/backend
# python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt

mysql -u root -p
CREATE DATABASE pet_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

python manage.py migrate

python manage.py runserver 0.0.0.0:8000


cd /Users/longyang/Desktop/code/demo/frontend
npm install
# 或
pnpm install
npm run dev






pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000


uvicorn app.main:app --reload --port 8000