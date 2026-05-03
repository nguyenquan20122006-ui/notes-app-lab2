from fastapi import APIRouter, HTTPException, Depends
 
from backend.app.schemas.note import NoteCreate, NoteResponse
from backend.app.dependencies.auth import get_current_user
from backend.app.services.firestore_service import save_note, load_notes, delete_note
 
router = APIRouter(prefix="/notes", tags=["Notes"])
 
 
@router.get("", response_model=list[NoteResponse])
def get_notes(user=Depends(get_current_user)):
    """
    Lấy danh sách ghi chú của user.
    Header: Authorization: Bearer <idToken>
    """
    notes = load_notes(user["uid"])
    return notes
 
 
@router.post("", response_model=dict)
def create_note(payload: NoteCreate, user=Depends(get_current_user)):
    """
    Tạo ghi chú mới và lưu vào Firestore.
    Header: Authorization: Bearer <idToken>
    Body: {title, content}
    """
    note_id = save_note(user["uid"], payload.title, payload.content)
    return {"id": note_id, "message": "Ghi chú đã được lưu thành công"}
 
 
@router.delete("/{note_id}", response_model=dict)
def remove_note(note_id: str, user=Depends(get_current_user)):
    """
    Xóa ghi chú theo ID (chỉ xóa được ghi chú của chính mình).
    Header: Authorization: Bearer <idToken>
    """
    result = delete_note(user["uid"], note_id)
 
    if result is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy ghi chú")
    if result is False:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa ghi chú này")
 
    return {"message": "Đã xóa ghi chú thành công"}