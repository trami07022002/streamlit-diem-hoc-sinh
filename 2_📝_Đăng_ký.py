import streamlit as st
import json
import os

st.set_page_config(page_title="Đăng ký")

st.title("📝 Đăng ký tài khoản")

# ---- Load database ----
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        try:
            users = json.load(f)

            # Nếu users là list => chuyển sang dict
            if isinstance(users, list):
                users = {}

        except:
            users = {}
else:
    users = {}

# ---- Form ----
username = st.text_input("Tên đăng nhập mới")
password = st.text_input("Mật khẩu", type="password")
role = st.selectbox("Vai trò:", ["GVCN", "Toan", "Anh", "Van", "Ly", "Hoa", "Sinh", "Tin"])

# ---- Register ----
if st.button("Tạo tài khoản"):

    if username in users:
        st.error("❌ Tài khoản đã tồn tại")
    else:
        users[username] = {"password": password, "role": role}

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        st.success("🎉 Đăng ký thành công! Mời đăng nhập.")
        st.switch_page("pages/1_🔐_Đăng_nhập.py")
