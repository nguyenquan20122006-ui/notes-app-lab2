"""
api_client.py
-------------
Toàn bộ lời gọi HTTP đến backend nằm ở đây.
app.py chỉ import và gọi hàm — không cần biết chi tiết HTTP.
 
ĐIỂM KHÁC SO VỚI V1:
  Token được truyền qua Authorization header (Bearer <token>)
  thay vì query parameter ?token=... — an toàn hơn nhiều.
"""
 
import requests
 
BACKEND_URL = "http://localhost:8000"
 
 
def _auth_header(id_token: str) -> dict:
    """Header chuẩn Bearer token — dùng cho mọi request cần xác thực."""
    return {"Authorization": f"Bearer {id_token}"}
 
 
# ── Auth ─────────────────────────────────────────────────────────────────────
 
def signup(email: str, password: str) -> dict:
    """Đăng ký tài khoản mới qua backend (Pyrebase4)."""
    r = requests.post(
        f"{BACKEND_URL}/auth/signup",
        json={"email": email, "password": password}
    )
    r.raise_for_status()
    return r.json()
 
 
def login(email: str, password: str) -> dict:
    """
    Đăng nhập qua backend (Pyrebase4).
    Trả về dict chứa: email, uid, idToken, refreshToken.
    """
    r = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={"email": email, "password": password}
    )
    r.raise_for_status()
    return r.json()
 
 
def get_me(id_token: str) -> dict:
    """Xác thực token hiện tại, trả về thông tin user."""
    r = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=_auth_header(id_token)
    )
    r.raise_for_status()
    return r.json()
 
 
# ── Notes ─────────────────────────────────────────────────────────────────────
 
def get_notes(id_token: str) -> list:
    """Lấy danh sách ghi chú của user hiện tại."""
    r = requests.get(
        f"{BACKEND_URL}/notes",
        headers=_auth_header(id_token)
    )
    r.raise_for_status()
    return r.json()
 
 
def create_note(id_token: str, title: str, content: str) -> dict:
    """Tạo ghi chú mới."""
    r = requests.post(
        f"{BACKEND_URL}/notes",
        json={"title": title, "content": content},
        headers=_auth_header(id_token)
    )
    r.raise_for_status()
    return r.json()
 
 
def delete_note(id_token: str, note_id: str) -> dict:
    """Xóa ghi chú theo ID."""
    r = requests.delete(
        f"{BACKEND_URL}/notes/{note_id}",
        headers=_auth_header(id_token)
    )
    r.raise_for_status()
    return r.json()