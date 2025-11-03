FROM python:3.11-slim

WORKDIR /app

# ติดตั้ง dependency พื้นฐาน
RUN apt-get update && apt-get install -y gcc libpq-dev

# คัดลอก requirements.txt
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

EXPOSE 8000

# คำสั่งรัน server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]