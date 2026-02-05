import streamlit as st
import time
import base64
import os

# Cấu hình trang
st.set_page_config(page_title="3LH Intro MAX", page_icon="🛡️", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

# --- HÀM HỖ TRỢ LOAD ẢNH ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

LOGO_FILENAME = "logo_3lh.png"
LOGO_ONLINE = "https://img.freepik.com/premium-vector/golden-shield-logo-design-vector-symbol-security-protection_460848-15024.jpg"
icon_base64 = get_image_base64(LOGO_FILENAME)
icon_url = f"data:image/png;base64,{icon_base64}" if icon_base64 else LOGO_ONLINE

# --- CSS HOẠT CẢNH (ĐÃ ĐỘ LẠI) ---
st.markdown(f"""
<style>
    /* Nền tối sang trọng, sâu hơn */
    .stApp {{
        background-color: #000000;
        background-image: radial-gradient(circle at center, #002244 0%, #000000 80%);
        color: #d4af37; font-family: 'Montserrat', sans-serif;
        overflow: hidden; /* Ẩn thanh cuộn nếu chữ quá to */
    }}

    /* [ĐIỀU CHỈNH 1] Quay 5 vòng = 1800 độ */
    @keyframes appearAndSpinMega {{
        0% {{ opacity: 0; transform: scale(0.05) rotateY(0deg); filter: blur(20px) brightness(0); }}
        20% {{ opacity: 1; filter: blur(0px) brightness(1); }} /* Hiện rõ nhanh hơn */
        100% {{ opacity: 1; transform: scale(1) rotateY(1800deg); filter: drop-shadow(0 0 80px #ffca28) brightness(1.2); }}
    }}

    /* Hiệu ứng chữ hiện ra */
    @keyframes textReveal {{
        from {{ opacity: 0; transform: scale(0.8) translateY(50px); filter: blur(10px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); filter: blur(0px); }}
    }}

    /* Áp dụng cho Logo */
    .intro-logo {{
        width: 400px; /* Logo to hơn chút */
        display: block; margin: 10vh auto 10px auto;
        /* [ĐIỀU CHỈNH THỜI GIAN] Tăng lên 5s để quay 5 vòng mượt mà */
        animation: appearAndSpinMega 5s cubic-bezier(0.1, 0.7, 0.1, 1) forwards;
    }}

    /* Áp dụng cho Chữ */
    /* Delay lâu hơn (4.5s) để chờ logo quay gần xong mới hiện chữ */
    .intro-text-box {{ text-align: center; animation: textReveal 2s ease-out forwards; animation-delay: 4.5s; opacity: 0; }}
    
    /* [ĐIỀU CHỈNH 2] Kích thước SIÊU TO KHỔNG LỒ (25rem) */
    .big-title {{
        font-family: 'Playfair Display', serif;
        font-size: 25rem; /* Gấp 5 lần cũ */
        font-weight: 900;
        color: #ffca28;
        margin-bottom: 0;
        line-height: 0.8; /* Ép dòng lại cho gọn */
        text-shadow: 0 0 100px rgba(255, 202, 40, 0.8); /* Hào quang chữ mạnh hơn */
        background: linear-gradient(to bottom, #ffca28, #ffeb3b, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .sub-title {{ font-size: 2rem; letter-spacing: 5px; text-transform: uppercase; color: #e6f1ff; margin-top: 20px; opacity: 0.8; }}
</style>
""", unsafe_allow_html=True)

# --- PHẦN HIỂN THỊ ---
placeholder = st.empty()

with placeholder.container():
    # 1. Logo xoay 5 vòng
    st.markdown(f'<img src="{icon_url}" class="intro-logo">', unsafe_allow_html=True)
    
    # 2. Chữ hiện ra siêu to
    st.markdown("""
        <div class="intro-text-box">
            <h1 class="big-title">3LH</h1>
            <p class="sub-title">BẢO CHỨNG NIỀM TIN SỐ</p>
        </div>
    """, unsafe_allow_html=True)

# Giữ màn hình lâu hơn chút để ngắm
time.sleep(15)
st.rerun()