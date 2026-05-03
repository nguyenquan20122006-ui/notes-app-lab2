from pydantic import BaseModel
 
 
class NoteCreate(BaseModel):
    title: str
    content: str
 
 
class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    uid: str