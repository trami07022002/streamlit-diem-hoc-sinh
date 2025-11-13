import streamlit as st
import json
import os

st.set_page_config(page_title="Đăng nhập")

st.title("🔐 Đăng nhập hệ thống")

# load user database
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

username = st.text_input("Tên đăng nhập")
password = st.text_input("Mật khẩu", type="password")

if st.button("Đăng nhập"):
    if username in users and users[username]["password"] == password:
        st.session_state["user"] = username
        st.session_state["role"] = users[username]["role"]

        st.success("🎉 Đăng nhập thành công!")
        st.switch_page("pages/3_📚_Nhập_điểm.py")
    else:
        st.error("❌ Sai tài khoản hoặc mật khẩu")

st.write("Nếu bạn chưa có tài khoản:")
if st.button("📝 Đăng ký"):
    st.switch_page("pages/2_📝_Đăng_ký.py")

