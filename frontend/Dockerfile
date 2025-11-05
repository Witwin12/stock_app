FROM node:20-alpine

# ตั้ง working directory
WORKDIR /app

# คัดลอก package.json ก่อน (จะช่วย cache install)
COPY package*.json ./

# ติดตั้ง dependencies
RUN npm install

# คัดลอกไฟล์ทั้งหมดเข้ามา
COPY . .

# เปิดพอร์ตของ Vite (5173 คือค่า default)
EXPOSE 5173

# คำสั่งรัน Vue dev server
CMD ["npm", "run", "dev"]
