## Thông tin sinh viên
- **Họ và tên:** Nguyễn Hữu Nghĩa  
- **Mã số sinh viên:** 24120104  
- **Môn học:** Tư duy tính toán  


#  Notes App — Bài thực hành Lab 2

Ứng dụng ghi chú đơn giản với **FastAPI** (backend) và **Streamlit** (frontend),
tích hợp **Firebase Authentication** (Pyrebase4) và **Firestore** database.

---

##  Cấu trúc thư mục

```
notes-app/
├── .streamlit/
│   └── secrets.toml              ← Firebase config (KHÔNG push lên GitHub)
├── backend/
│   └── app/
│       ├── core/
│       │   └── firebase_config.py
│       ├── dependencies/
│       │   └── auth.py
│       ├── routers/
│       │   ├── auth.py
│       │   └── notes.py
│       ├── schemas/
│       │   ├── auth.py
│       │   └── note.py
│       ├── services/
│       │   └── firestore_service.py
│       └── main.py
├── frontend/
│   ├── api_client.py
│   └── app.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

##  Cài đặt environment

```bash
# 1. Clone repo
git clone <your-repo-url>
cd notes-app

# 2. Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Kích hoạt (Mac/Linux)
source .venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt
```

---

##  Cấu hình Firebase (bắt buộc trước khi chạy)

1. Vào [Firebase Console](https://console.firebase.google.com) → tạo project
2. Bật **Authentication → Email/Password**
3. Tạo **Firestore Database** (production mode + cập nhật rules)
4. Vào  **Project Settings → Service accounts → Generate new private key**
5. Vào  **Project Settings → General** → copy `firebaseConfig`

Tạo file `.streamlit/secrets.toml` (không push file này lên GitHub):

```toml
[firebase_client]
apiKey = "..."
authDomain = "..."
projectId = "..."
storageBucket = "..."
messagingSenderId = "..."
appId = "..."
databaseURL = "..."

[firebase_admin]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

---

##  Chạy Backend

```bash
# Từ thư mục gốc, đã activate venv
uvicorn backend.app.main:app --reload
```

- API chạy tại: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

---

##  Chạy Frontend

Mở terminal mới (cùng venv đã activate):

```bash
streamlit run frontend/app.py
```

- Giao diện tại: http://localhost:8501

---

##  Video Demo

>  [Link video demo](https://youtu.be/BKFDwDIx2wM)

---

##  Tính năng

- Đăng ký / Đăng nhập bằng Firebase Authentication (Email/Password)
- Token xác thực qua `Authorization: Bearer` header
- Thêm ghi chú mới (tiêu đề + nội dung)
- Xem danh sách ghi chú (mới nhất lên đầu)
- Xóa ghi chú
- Dữ liệu lưu trên Firestore, phân theo từng user