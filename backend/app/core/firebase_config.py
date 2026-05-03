import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
 
 
def get_pyrebase_auth():
    """
    Khởi tạo Pyrebase từ secrets.toml và trả về auth client.
    Dùng để đăng ký / đăng nhập bằng email-password trong backend.
    """
    firebase_cfg = dict(st.secrets["firebase_client"])
    firebase_app = pyrebase.initialize_app(firebase_cfg)
    return firebase_app.auth()
 
 
def init_firebase_admin():
    """
    Khởi tạo Firebase Admin SDK từ secrets.toml.
    Chỉ khởi tạo một lần duy nhất (kiểm tra _apps trước).
    """
    if not firebase_admin._apps:
        cred_dict = dict(st.secrets["firebase_admin"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
 
 
def get_firestore():
    """Đảm bảo Admin đã init rồi trả về Firestore client."""
    init_firebase_admin()
    return firestore.client()