import streamlit as st
import json
import os

st.title("📝 Đăng ký tài khoản")

username = st.text_input("Tên đăng nhập mới")
password = st.text_input("Mật khẩu", type="password")
role = st.selectbox("Vai trò:", ["GVCN", "Toan", "Van", "Anh", "Ly", "Hoa"])

# Load users
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

if st.button("Tạo tài khoản"):
    if username in users:
        st.error("⚠️ Tên đăng nhập đã tồn tại!")
    else:
        users[username] = {"password": password, "role": role}
        with open("users.json", "w") as f:
            json.dump(users, f)

        st.success("🎉 Tạo tài khoản thành công!")
        st.switch_page("pages/1_Dang_nhap.py")
