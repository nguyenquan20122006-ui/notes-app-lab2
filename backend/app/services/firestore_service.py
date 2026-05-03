from datetime import datetime, timezone
from firebase_admin import firestore
from backend.app.core.firebase_config import get_firestore
 
db = get_firestore()
 
 
def save_note(uid: str, title: str, content: str) -> str:
    """Lưu ghi chú mới vào Firestore, trả về document ID."""
    doc_ref = db.collection("notes").document()
    doc_ref.set({
        "uid": uid,
        "title": title,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return doc_ref.id
 
 
def load_notes(uid: str) -> list[dict]:
    """Lấy tất cả ghi chú của user, sắp xếp mới nhất lên đầu."""
    docs = (
        db.collection("notes")
        .where("uid", "==", uid)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]
 
 
def delete_note(uid: str, note_id: str) -> bool:
    """
    Xóa ghi chú theo ID.
    Kiểm tra quyền sở hữu trước khi xóa — trả về False nếu không có quyền.
    """
    doc_ref = db.collection("notes").document(note_id)
    doc = doc_ref.get()
 
    if not doc.exists:
        return None                        # không tìm thấy
 
    if doc.to_dict().get("uid") != uid:
        return False                       # không có quyền
 
    doc_ref.delete()
    return True                            # xóa thành công