from fastapi import APIRouter, HTTPException, Depends
 
from backend.app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from backend.app.core.firebase_config import get_pyrebase_auth, init_firebase_admin
from backend.app.dependencies.auth import get_current_user
 
router = APIRouter(prefix="/auth", tags=["Authentication"])
 
# Khởi tạo một lần khi module được load
auth_client = get_pyrebase_auth()
init_firebase_admin()
 
 
@router.post("/signup")
def signup(payload: SignupRequest):
    """
    Đăng ký tài khoản mới bằng Pyrebase4.
    Frontend gọi: POST /auth/signup  body: {email, password}
    """
    try:
        auth_client.create_user_with_email_and_password(
            payload.email, payload.password
        )
        return {"message": "Tạo tài khoản thành công"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
 
@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    """
    Đăng nhập bằng Pyrebase4 — trả về idToken để frontend lưu vào session.
    Frontend gọi: POST /auth/login  body: {email, password}
    """
    try:
        user = auth_client.sign_in_with_email_and_password(
            payload.email, payload.password
        )
        return AuthResponse(
            email=payload.email,
            uid=user["localId"],
            idToken=user["idToken"],
            refreshToken=user.get("refreshToken")
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
 
 
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    """
    Kiểm tra token hiện tại.
    Frontend gọi: GET /auth/me  header: Authorization: Bearer <token>
    """
    return {
        "uid": user["uid"],
        "email": user["email"]
    }