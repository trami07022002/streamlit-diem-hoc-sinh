import streamlit as st

st.set_page_config(page_title="Hệ thống quản lý điểm học sinh", layout="wide")

st.title("🏫 Hệ thống quản lý điểm học sinh")
st.write("Chọn chức năng bên dưới:")

if st.button("🔐 Đăng nhập"):
    st.switch_page("pages/1_Dang_nhap.py")

if st.button("📝 Đi đến trang nhập điểm"):
    st.switch_page("pages/3_Nhap_diem.py")
