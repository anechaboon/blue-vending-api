# FastAPI Project

## 1. Requirements

- Python 3.11+
- pip
- PostgreSQL

## 2. การติดตั้งและตั้งค่า

1. **สร้าง virtual environment**

```bash
python3.11 -m venv venv
```

2. **เปิดใช้งาน virtual environment**

```bash
source venv/bin/activate
```

3. **ติดตั้ง dependencies**

```bash
pip install -r app/requirements.txt
```

4. **ตั้งค่า environment variables** สร้างไฟล์ `.env` ใน root ของโปรเจกต์ (ตัวอย่าง):

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
```

## 3. การรันเซิร์ฟเวอร์

```bash
uvicorn app.main:app --reload
```

เปิดเบราว์เซอร์ที่ `http://127.0.0.1:8000/docs` เพื่อดู Swagger UI

## 4. การรันเทส&#x20;

```bash
pytest --cov=app
```

## 5. ตัวอย่าง API

- `GET /items/` → ดึงรายการทั้งหมด
- `POST /items/` → สร้างรายการใหม่
- `GET /items/{id}` → ดึงรายการตาม ID
- `PUT /items/{id}` → อัปเดตรายการ
- `DELETE /items/{id}` → ลบรายการ

## 6. Tips

- ใช้ `source venv/bin/activate` ทุกครั้งก่อนรันคำสั่ง Python



