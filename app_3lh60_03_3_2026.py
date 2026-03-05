import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH HỆ THỐNG (GOLD STANDARD) ---
st.set_page_config(
    page_title="3LH1 - CORE ESCROW SYSTEM",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GIAO DIỆN HOÀNG GIA (ROYAL NAVY & GOLD) ---
st.markdown("""
<style>
    /* Nền chính - Xanh Navy đậm */
    .stApp { background-color: #051622; color: #EDEADE; }
    
    /* Tiêu đề Vàng kim loại */
    h1, h2, h3, h4 { color: #DEB887 !important; font-family: 'Times New Roman', serif; }
    
    /* Tabs (Lớp) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #1E2A38; border-radius: 5px; color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #DEB887; color: black !important; font-weight: bold;
    }
    
    /* Input & Card */
    .stTextInput > div > div > input { color: #fff; background-color: #262730; border: 1px solid #DEB887; }
    div[data-testid="stMetricValue"] { color: #00FF00; }
    
    /* Button */
    div.stButton > button {
        background: linear-gradient(to right, #DAA520, #FFD700); color: black; font-weight: bold; border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE GIẢ LẬP (LƯU TRỮ ĐA LỚP) ---
if 'escrow_transactions' not in st.session_state:
    st.session_state.escrow_transactions = {}

if 'db_layer2' not in st.session_state: 
    st.session_state.db_layer2 = {} # Travel Shield

# --- 4. HÀM SINH MÃ ĐỊNH DANH (THEO LỚP) ---
def generate_code(layer_prefix):
    # Layer 1: 3LH1-GEN (General) | Layer 2: 3LH1-TRV (Travel)
    suffix = random.randint(10000, 99999)
    return f"{layer_prefix}-{suffix}"

# --- 5. GIAO DIỆN CHÍNH ---
st.title("🏛️ 3LH1 TRUST CORE")
st.caption("HỆ THỐNG BẢO LÃNH TÍN NHIỆM ĐA TẦNG (MULTI-LAYER ESCROW)")
st.markdown("---")


# ==============================================================================
# KHỞI TẠO CÁC LỚP (LAYERS)
# ==============================================================================
layer1, layer2 = st.tabs([
    "📂 LAYER 1: HỢP ĐỒNG THƯƠNG MẠI (GENERAL)", 
    "✈️ LAYER 2: TRAVEL SHIELD (DU LỊCH)"
])

# ==============================================================================
# LAYER 1: HỢP ĐỒNG THƯƠNG MẠI (MUA BÁN, BẤT ĐỘNG SẢN, HỢP TÁC)
# ==============================================================================
with layer1:
    # -------------------------------------------------------------
    # TOÀN BỘ CODE CŨ (400 DÒNG) ĐÃ ĐƯỢC CHÈN VÀO ĐÂY VÀ THỤT LỀ
    # -------------------------------------------------------------
    
    # HÀM TẠO MÃ GIAO DỊCH 3LH (Dùng code cũ)
    def generate_3lh_code():
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return '3LH-' + ''.join(random.choice(chars) for _ in range(8))

    # GIAO DIỆN CHÍNH
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://img.icons8.com/color/96/000000/shield.png", width=80)
    with col2:
        st.title("HỆ THỐNG BẢO LÃNH GIAO DỊCH")
        st.subheader("Phiên bản thử nghiệm (Mockup)")

    # CHIA TAB: BÊN MUA | BÊN BÁN | TRA CỨU
    tab1, tab2, tab3 = st.tabs(["🛒 BÊN MUA (TẠO LỆNH)", "🏪 BÊN BÁN (KIỂM TRA)", "🔍 LỊCH SỬ GIAO DỊCH"])

    # ---------------- TAB 1: BÊN MUA (NGƯỜI CHUYỂN TIỀN) ----------------
    with tab1:
        st.markdown("### 📝 THIẾT LẬP GIAO DỊCH MỚI")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            buyer_name = st.text_input("Tên Bên Mua:", placeholder="VD: Nguyễn Văn A")
            seller_contact = st.text_input("SĐT/Zalo Bên Bán (Người nhận):", placeholder="VD: 090xxxxxxx")
            
        with col_m2:
            amount = st.number_input("Số tiền giao dịch (VNĐ):", min_value=10000, value=500000, step=50000, format="%d")
            product_info = st.text_area("Thông tin hàng hóa/dịch vụ:", placeholder="VD: Mua acc game, chuyển khoản cọc áo...")

        if st.button("🚀 TẠO LỆNH BẢO LÃNH (CHUYỂN TIỀN VÀO 3LH)", use_container_width=True):
            if not buyer_name or not seller_contact or not product_info:
                st.warning("⚠️ Vui lòng điền đầy đủ thông tin giao dịch.")
            else:
                with st.spinner("Đang xử lý giao dịch vào hệ thống 3LH..."):
                    time.sleep(1.5) # Giả lập độ trễ mạng
                    
                    tx_code = generate_3lh_code()
                    
                    # Lưu vào Database giả lập (Session State)
                    st.session_state.escrow_transactions[tx_code] = {
                        "buyer": buyer_name,
                        "seller": seller_contact,
                        "amount": amount,
                        "product": product_info,
                        "status": "LOCKED (TIỀN ĐANG BỊ KHÓA BỞI 3LH)",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.success("✅ GIAO DỊCH ĐÃ ĐƯỢC BẢO LÃNH THÀNH CÔNG!")
                    
                    # Hiển thị hóa đơn (Mockup)
                    st.markdown("---")
                    st.markdown(f"### MÃ GIAO DỊCH: **`{tx_code}`**")
                    st.info(f"""
                    **Hướng dẫn tiếp theo:**
                    1. Giao dịch trị giá **{amount:,.0f} VNĐ** đã được 3LH đóng băng.
                    2. Hãy gửi **MÃ GIAO DỊCH** này cho Bên Bán.
                    3. Yêu cầu Bên Bán vào Tab 'BÊN BÁN' để kiểm tra. Nếu họ thấy chữ **LOCKED**, họ có thể yên tâm giao hàng.
                    """)

    # ---------------- TAB 2: BÊN BÁN (NGƯỜI NHẬN TIỀN) ----------------
    with tab2:
        st.markdown("### 🔍 KIỂM TRA MÃ BẢO LÃNH")
        st.write("Nhập Mã Giao Dịch do Bên Mua cung cấp để xác nhận tiền đã vào hệ thống 3LH chưa.")
        
        search_code = st.text_input("Nhập Mã Giao Dịch (Ví dụ: 3LH-XXXXXXXX):")
        
        if st.button("KIỂM TRA TRẠNG THÁI TIỀN", use_container_width=True):
            if not search_code:
                st.warning("Vui lòng nhập mã.")
            elif search_code in st.session_state.escrow_transactions:
                tx_data = st.session_state.escrow_transactions[search_code]
                
                st.success("✅ MÃ HỢP LỆ. TIỀN ĐÃ CÓ TRONG HỆ THỐNG.")
                
                # Hiển thị thông tin
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.metric("Người gửi (Bên Mua):", tx_data["buyer"])
                    st.metric("Số tiền bảo lãnh:", f"{tx_data['amount']:,.0f} VNĐ")
                with col_b2:
                    st.metric("Trạng thái:", tx_data["status"], delta="An toàn", delta_color="normal")
                    st.metric("Hàng hóa:", tx_data["product"])
                    
                st.info("💡 **Ghi chú cho Bên Bán:** Tiền đã được khóa an toàn. Bạn hãy tiến hành giao hàng. Sau khi Bên Mua xác nhận nhận đủ hàng, tiền sẽ lập tức được mở khóa và chuyển vào tài khoản của bạn.")
            else:
                st.error("❌ MÃ KHÔNG TỒN TẠI. VUI LÒNG CẢNH GIÁC TRÁNH BỊ LỪA ĐẢO GIAO HÀNG.")

    # ---------------- TAB 3: LỊCH SỬ GIAO DỊCH CỦA HỆ THỐNG ----------------
    with tab3:
        st.markdown("### 📊 DỮ LIỆU ĐANG ĐƯỢC 3LH BẢO LÃNH (REALTIME)")
        if not st.session_state.escrow_transactions:
            st.write("Chưa có giao dịch nào.")
        else:
            # Chuyển Dict sang List để hiển thị thành bảng
            tx_list = []
            for code, data in st.session_state.escrow_transactions.items():
                tx_list.append({
                    "Mã Giao Dịch": code,
                    "Bên Mua": data["buyer"],
                    "Bên Bán (SĐT)": data["seller"],
                    "Số tiền (VNĐ)": f"{data['amount']:,.0f}",
                    "Trạng thái": data["status"],
                    "Thời gian": data["date"]
                })
            
            import pandas as pd
            df = pd.DataFrame(tx_list)
            st.dataframe(df, use_container_width=True)

# ==============================================================================
# LAYER 2: TRAVEL SHIELD (DÀNH RIÊNG CHO ĐẶT PHÒNG/DU LỊCH)
# ==============================================================================
with layer2:
    st.markdown("### 🛡️ KHIÊN BẢO VỆ DU LỊCH (TRAVEL SHIELD)")
    st.caption("Cơ chế: Cọc Treo (Escrow) - Tiền chỉ chuyển khi Check-in thành công.")
    
    # Chia 2 cột: Bên Trái (Khách tạo lệnh) - Bên Phải (Chủ nhà check)
    l2_col1, l2_col2 = st.columns(2)
    
    # --- CỘT TRÁI: KHÁCH HÀNG ---
    with l2_col1:
        st.markdown("#### 1. DÀNH CHO KHÁCH (TẠO CỌC)")
        with st.form("travel_form"):
            t_guest = st.text_input("Họ tên Khách:", "Vương Văn Luân")
            t_host_contact = st.text_input("SĐT/Zalo Chủ Homestay:")
            t_amount = st.number_input("Số tiền cọc (VNĐ):", value=500000, step=50000)
            t_date = st.date_input("Ngày Check-in:", datetime.now() + timedelta(days=1))
            t_note = st.text_input("Ghi chú (Tên phòng/Resort):", "Cọc phòng Vũng Tàu")
            
            submitted = st.form_submit_button("🚀 KÍCH HOẠT BẢO LÃNH DU LỊCH")
            
            if submitted and t_host_contact:
                t_code = generate_code("3LH1-TRV")
                st.session_state.db_layer2[t_code] = {
                    "guest": t_guest, "host": t_host_contact, "amount": t_amount,
                    "date": t_date.strftime("%d/%m/%Y"), "status": "SAFE_HOLD"
                }
                st.success("✅ Đã tạo Mã Bảo Lãnh!")
                st.code(t_code, language="text")
                st.warning("👉 Hãy gửi mã này cho Chủ nhà để xác nhận phòng.")

    # --- CỘT PHẢI: CHỦ NHÀ ---
    with l2_col2:
        st.markdown("#### 2. DÀNH CHO CHỦ nhà (KIỂM TRA)")
        st.info("Chủ nhà nhập mã khách gửi để kiểm tra xem Tiền đã vào hệ thống 3LH chưa.")
        
        t_search = st.text_input("Nhập Mã Bảo Lãnh (3LH1-TRV...):")
        if st.button("🔍 KIỂM TRA CỌC"):
            if t_search in st.session_state.db_layer2:
                dt = st.session_state.db_layer2[t_search]
                st.markdown(f"""
                <div style="border: 2px solid #00FF00; padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: #00FF00; margin:0;">XÁC THỰC THÀNH CÔNG</h2>
                    <p style="color:white;">Mã lệnh: <b>{t_search}</b></p>
                    <hr style="border-color: #555;">
                    <h1 style="color: #DEB887;">{dt['amount']:,.0f} VNĐ</h1>
                    <p style="color: #aaa;">Khách hàng: {dt['guest']}</p>
                    <p style="color: #aaa;">Ngày Check-in: {dt['date']}</p>
                    <br>
                    <button style="background-color: #333; color: white; border: 1px solid white; padding: 5px 10px;">TRẠNG THÁI: ĐANG GIỮ TIỀN</button>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⛔ Mã không tồn tại! Cảnh báo lừa đảo.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='color: #666;'>🔒 3LH1 Core Engine | Architecture v2.0 (Multi-Layer)</center>", unsafe_allow_html=True)