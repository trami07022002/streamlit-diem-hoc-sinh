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

# Tạo cột điểm & ghi chú nếu thiếu
for sub in subjects:
    if sub not in df.columns:
        df[sub] = None
    note_col = f"Ghi_chu_{sub}"
    if note_col not in df.columns:
        df[note_col] = ""

# Tạo cột tổng hợp nếu thiếu
if "Tong_hop" not in df.columns:
    df["Tong_hop"] = ""

# ----------------------------
# ⭐ PHÂN QUYỀN
# ----------------------------

if role == "GVCN":
    # GVCN xem toàn bộ nhưng chỉ nhập cột Tổng hợp
    editable_cols = ["Tong_hop"]
    disabled_cols = [c for c in df.columns if c not in editable_cols]

    st.info(
        "🧑‍🏫 **GVCN chỉ được nhập cột Tổng hợp.**\n"
        "Các cột điểm & ghi chú của GV bộ môn sẽ hiển thị để xem."
    )

elif role in subjects:
    # Giáo viên bộ môn chỉ xem thông tin & cột của mình
    editable_cols = [role, f"Ghi_chu_{role}"]

    required_cols = ["STT", "Ho_va_ten", "Ngay_sinh", "Gioi_tinh"] + editable_cols
    df = df[required_cols]

    disabled_cols = [c for c in df.columns if c not in editable_cols]

    st.info(f"👨‍🏫 Bạn đang nhập điểm môn **{role}**.")

else:
    st.error("❌ Vai trò không hợp lệ.")
    st.stop()


# ----------------------------
# ⭐ BẢNG NHẬP LIỆU
# ----------------------------
edited_df = st.data_editor(
    df,
    hide_index=True,
    use_container_width=True,
    disabled=disabled_cols
)

# ----------------------------
# ⭐ LƯU FILE
# ----------------------------

if st.button("💾 Lưu dữ liệu"):
    original = pd.read_excel(file_path)

    if role == "GVCN":
        original["Tong_hop"] = edited_df["Tong_hop"]

    elif role in subjects:
        # Gộp lại đúng hàng theo STT
        # → cực quan trọng để tránh lệch dữ liệu !!!
        for col in [role, f"Ghi_chu_{role}"]:
            original[col] = original.merge(
                edited_df[["STT", col]],
                on="STT",
                how="left"
            )[col + "_y"]

    original.to_excel(file_path, index=False)
    st.success("✔ Đã lưu thành công!")
