# 🛒 Stock Management App  
ระบบบริหารจัดการสต็อกสินค้า (Django REST + Vue.js + Docker)

โปรเจกต์นี้ประกอบด้วย Backend (Django REST Framework) และ Frontend (Vue 3 + Vite) ทำงานร่วมกันด้วย Docker Compose พร้อมฐานข้อมูล PostgreSQL


## 📁 โครงสร้างโปรเจกต์
```
├── backend
│ ├── stocks_app
│ │ ├── migrations
│ │ ├── models
│ │ ├── serializers
│ │ ├── tests
│ │ ├── views
│ │ └── pycache
│ └── stock_api
│ └── pycache
│
└── frontend
├── .vscode
├── node_modules
├── public
└── src
├── api
├── assets
├── components
├── composables
├── router
└── views
docker-compose.yml
```

---

## 🧰 เทคโนโลยีที่ใช้

### **Backend**
- Django 5 + Django REST Framework  
- Python 3.11  
- PostgreSQL

### **Frontend**
- Vue 3 + Vite  
- Vue Router  
- Axios  
- Composition API  

### **Infrastructure**
- Docker  
- Docker Compose

---

## ⚙️ การตั้งค่าเริ่มต้น
```
สร้างไฟล์ `.env` ไว้ที่ root:


backend/Dockerfile
frontend/Dockerfile

POSTGRES_DB=stockdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db

DJANGO_SETTINGS_MODULE=stock_api.settings

NODE_ENV=development
DJANGO_SECRET_KEY=YOUR SECRECT KEY
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
```

---

## ▶️ วิธีรันโปรเจกต์ด้วย Docker

### 1. Build และรันทั้งหมด
```
docker compose up --build
```

### 2. เปิดเว็บใช้งาน

| Service | URL |
|--------|-----|
| Django API | http://localhost:8000 |
| Vue Frontend | http://localhost:5173 |



## 🧹 ล้าง Container + Volume
```
docker compose down --volumes
```

## สำหรับ production 
```
docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
```

 เปิดเว็บใช้งาน

| Service | URL |
|--------|-----|
|Web | http://localhost |
|AdminPage | http://localhost/admin |

