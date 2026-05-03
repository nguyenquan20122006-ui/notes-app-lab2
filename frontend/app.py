"""
app.py
------
Giao diện Streamlit cho Notes App.
Mọi lời gọi API đều thông qua api_client.py.
Login / Signup gọi qua backend (Pyrebase4) — KHÔNG gọi Firebase REST trực tiếp.
"""
 
import sys
import os
 
sys.path.insert(0, os.path.dirname(__file__))
 
import requests
import streamlit as st
from api_client import signup, login, get_notes, create_note, delete_note
 
# ── Cấu hình trang ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Notes App",
    page_icon="📝",
    layout="centered"
)
 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1 { font-family: 'DM Serif Display', serif !important; }
    .note-card {
        background: #fffdf5;
        border: 1px solid #e8e0cc;
        border-left: 4px solid #c8a97e;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .note-title { font-weight: 600; font-size: 1.05rem; color: #2c1e0f; margin-bottom: 6px; }
    .note-content { color: #5a4a3a; font-size: 0.92rem; line-height: 1.6; }
    .note-date { color: #a08060; font-size: 0.78rem; margin-top: 8px; }
    section[data-testid="stSidebar"] { background-color: #faf6ef; border-right: 1px solid #e8e0cc; }
</style>
""", unsafe_allow_html=True)
 
# ── Khởi tạo session state ────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None          # dict: {uid, email, idToken}
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
 
 
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📝 Notes App")
    st.divider()
 
    # Chưa đăng nhập → hiện form
    if st.session_state.user is None:
 
        if st.session_state.show_signup:
            # ── Form đăng ký ──────────────────────────────────────────────
            st.markdown("### Đăng ký")
            with st.form("signup_form"):
                email = st.text_input("Email")
                password = st.text_input("Mật khẩu", type="password")
                submitted = st.form_submit_button("Tạo tài khoản", use_container_width=True, type="primary")
                go_login = st.form_submit_button("Đã có tài khoản? Đăng nhập", use_container_width=True)
 
            if go_login:
                st.session_state.show_signup = False
                st.rerun()
 
            if submitted:
                try:
                    signup(email, password)
                    st.success("✅ Tạo tài khoản thành công! Hãy đăng nhập.")
                    st.session_state.show_signup = False
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"❌ {e.response.json().get('detail', str(e))}")
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
 
        else:
            # ── Form đăng nhập ─────────────────────────────────────────────
            st.markdown("### Đăng nhập")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Mật khẩu", type="password")
                submitted = st.form_submit_button("Đăng nhập", use_container_width=True, type="primary")
                go_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký", use_container_width=True)
 
            if go_signup:
                st.session_state.show_signup = True
                st.rerun()
 
            if submitted:
                try:
                    # Gọi backend → backend dùng Pyrebase4 xử lý
                    result = login(email, password)
                    st.session_state.user = result   # lưu {uid, email, idToken}
                    st.success("✅ Đăng nhập thành công!")
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"❌ {e.response.json().get('detail', 'Sai email hoặc mật khẩu')}")
                except Exception as e:
                    st.error(f"❌ Không thể kết nối backend: {e}")
 
    # Đã đăng nhập → hiện thông tin + form thêm ghi chú
    else:
        user = st.session_state.user
        st.success(f"👤 {user['email']}")
        st.divider()
 
        st.markdown("**Thêm ghi chú mới**")
        note_title = st.text_input("Tiêu đề", placeholder="Tiêu đề ghi chú...")
        note_content = st.text_area("Nội dung", placeholder="Nội dung...", height=150)
 
        if st.button("💾 Lưu ghi chú", use_container_width=True, type="primary"):
            if note_title and note_content:
                try:
                    create_note(user["idToken"], note_title, note_content)
                    st.success("✅ Đã lưu!")
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"❌ {e.response.json().get('detail', 'Lỗi lưu')}")
                except Exception as e:
                    st.error(f"❌ Không thể kết nối backend: {e}")
            else:
                st.warning("Vui lòng nhập đầy đủ tiêu đề và nội dung")
 
        st.divider()
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.rerun()
 
 
# ── Nội dung chính ────────────────────────────────────────────────────────────
st.title("📝 Ghi chú của tôi")
 
if st.session_state.user is None:
    st.info("👈 Vui lòng đăng nhập ở thanh bên trái để bắt đầu.")
    st.stop()
 
# Tải danh sách ghi chú
try:
    with st.spinner("Đang tải ghi chú..."):
        notes = get_notes(st.session_state.user["idToken"])
except Exception:
    st.error("❌ Không thể tải ghi chú. Kiểm tra backend đã chạy chưa.")
    st.stop()
 
if not notes:
    st.markdown("""
    <div style='text-align:center;padding:60px 0;color:#a08060'>
        <div style='font-size:3rem'>📭</div>
        <div style='font-size:1.1rem;margin-top:12px'>Chưa có ghi chú nào.</div>
        <div style='font-size:0.9rem'>Thêm ghi chú đầu tiên từ thanh bên trái!</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"**{len(notes)} ghi chú**")
    st.divider()
 
    for note in notes:
        st.markdown(f"""
        <div class="note-card">
            <div class="note-title">📌 {note['title']}</div>
            <div class="note-content">{note['content']}</div>
            <div class="note-date">🕐 {note.get('created_at','')[:19].replace('T',' ')}</div>
        </div>
        """, unsafe_allow_html=True)
 
        if st.button("🗑️ Xóa", key=f"del_{note['id']}"):
            try:
                delete_note(st.session_state.user["idToken"], note["id"])
                st.success("Đã xóa")
                st.rerun()
            except requests.HTTPError as e:
                st.error(f"❌ {e.response.json().get('detail', 'Lỗi xóa')}")