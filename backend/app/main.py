from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from backend.app.routers.auth import router as auth_router
from backend.app.routers.notes import router as notes_router
 
app = FastAPI(
    title="Notes App API",
    description="Backend cho ứng dụng ghi chú — Bài lab 2",
    version="1.0.0"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(auth_router)
app.include_router(notes_router)
 
 
@app.get("/", tags=["General"])
def root():
    return {"message": "Notes App API đang chạy ✅"}
 
 
@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}