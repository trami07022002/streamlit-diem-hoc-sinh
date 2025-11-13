import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Nhập điểm", layout="wide")

# ---- Kiểm tra login ----
if "user" not in st.session_state:
    st.error("⚠ Bạn chưa đăng nhập.")
    st.stop()

username = st.session_state["user"]
role = st.session_state["role"]

st.title(f"📚 Chế độ: **{role}**")

# ---- Load file Excel ----
file_path = "danh_sach_hoc_sinh_2008.xlsx"
df = pd.read_excel(file_path)

# Danh sách môn
subjects = ["Toan", "Anh", "Van", "Ly", "Hoa", "Sinh", "Tin"]

# Tạo cột ghi chú nếu chưa có
for sub in subjects:
    note_col = f"Ghi_chu_{sub}"
    if note_col not in df.columns:
        df[note_col] = ""

# ----------------------------
# ⭐ PHÂN QUYỀN HIỂN THỊ VÀ NHẬP
# ----------------------------

if role == "GVCN":
    # GVCN chỉ nhập được 1 cột Tổng hợp
    editable_cols = ["Tong_hop"]

    # Các cột khác chỉ để xem
    disabled_cols = [c for c in df.columns if c not in editable_cols]

    st.info("🧑‍🏫 **GVCN chỉ được nhập cột Tổng hợp**.\nCác cột khác hiển thị để xem kết quả từ giáo viên bộ môn.")

elif role in subjects:
    # Giáo viên bộ môn: chỉ được nhập điểm + ghi chú của môn mình
    editable_cols = [role, f"Ghi_chu_{role}"]

    # Ẩn tất cả môn khác
    allowed_view = ["STT", "Ho_va_ten", "Ngay_sinh", "Gioi_tinh"] + editable_cols

    df = df[allowed_view]

    disabled_cols = [c for c in df.columns if c not in editable_cols]

    st.info(f"👨‍🏫 Bạn đang nhập điểm môn **{role}**.")

else:
    st.error("Vai trò không hợp lệ.")
    st.stop()

# ----------------------------
# ⭐ BẢNG NHẬP LIỆU
# ----------------------------
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    disabled=disabled_cols
)

# ----------------------------
# ⭐ LƯU FILE
# ----------------------------

if st.button("💾 Lưu dữ liệu"):
    # Đọc lại file gốc, vì giáo viên bộ môn chỉ nhìn thấy 1 phần bảng
    original = pd.read_excel(file_path)

    if role == "GVCN":
        original["Tong_hop"] = edited_df["Tong_hop"]

    elif role in subjects:
        original[role] = edited_df[role]
        original[f"Ghi_chu_{role}"] = edited_df[f"Ghi_chu_{role}"]

    original.to_excel(file_path, index=False)
    st.success("✔ Đã lưu thành công!")
