import streamlit as st
import time
import os
import datetime
from datetime import timedelta
import base64
import sqlite3
import bcrypt
import requests
from PIL import Image

# ==========================================
# 1. CẤU HÌNH & XỬ LÝ LOGO THÔNG MINH
# ==========================================
# --- CẤU HÌNH THANH TOÁN (SEPAY) ---
SEPAY_API_TOKEN = "HAY_DIEN_API_TOKEN_CUA_ANH_VAO_DAY" 
MY_BANK_ACCOUNT = "0368866xxx"
MY_BANK_NAME = "MBBank"
DB_NAME = "3lh_ledger_v103_full.db"

# --- XỬ LÝ FILE ẢNH LOGO ---
def get_image_base64(path):
    """Chuyển file ảnh thành mã Base64 để hiển thị trong HTML"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

LOGO_FILE_NEW = "logo_icon.png"
LOGO_FILE_OLD = "logo_3lh.png"
LOGO_ONLINE = "https://img.freepik.com/premium-vector/golden-shield-logo-design-vector-symbol-security-protection_460848-15024.jpg"

# Ưu tiên tìm logo icon mới
if os.path.exists(LOGO_FILE_NEW):
    CURRENT_LOGO = LOGO_FILE_NEW
elif os.path.exists(LOGO_FILE_OLD):
    CURRENT_LOGO = LOGO_FILE_OLD
else:
    CURRENT_LOGO = None

# Tạo URL cho ảnh xoay (HTML)
if CURRENT_LOGO:
    icon_base64 = get_image_base64(CURRENT_LOGO)
    icon_url = f"data:image/png;base64,{icon_base64}"
else:
    icon_url = LOGO_ONLINE

# Cấu hình Tab trình duyệt (Favicon)
try:
    if os.path.exists(LOGO_FILE_NEW):
        img_icon = Image.open(LOGO_FILE_NEW)
        st.set_page_config(page_title="3LH Global Escrow", page_icon=img_icon, layout="wide")
    else:
        st.set_page_config(page_title="3LH Global Escrow", page_icon="🛡️", layout="wide")
except:
    st.set_page_config(page_title="3LH Global Escrow", page_icon="🛡️", layout="wide")

# ==========================================
# 2. CSS GIAO DIỆN (CHUYÊN NGHIỆP)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Montserrat:wght@400;600;800;900&display=swap');
    
    /* TỔNG THỂ */
    .stApp { 
        background-color: #003366; 
        background-image: linear-gradient(135deg, #003366 0%, #00509e 100%); 
        color: #e6f1ff; 
        font-family: 'Montserrat', sans-serif; 
    }
    
    /* HIỆU ỨNG LOGO XOAY 3D */
    @keyframes rotationY { 
        from { transform: perspective(1000px) rotateY(0deg); } 
        to { transform: perspective(1000px) rotateY(360deg); } 
    }
    .rotating-logo { 
        animation: rotationY 15s infinite linear; 
        display: block; 
        margin-left: auto; margin-right: auto; 
        filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.6)); 
        transform-style: preserve-3d; 
    }
    
    /* HIỆU ỨNG INTRO */
    @keyframes spinShieldFiveTimes {
        0% { opacity: 0; transform: scale(0.5) rotateY(0deg); filter: blur(5px); }
        20% { opacity: 1; filter: blur(0px); }
        100% { opacity: 1; transform: scale(1.2) rotateY(1800deg); filter: drop-shadow(0 0 50px #ffca28); }
    }
    .intro-spinning-logo {
        display: block; margin: 15vh auto; width: 300px;
        animation: spinShieldFiveTimes 4.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    .intro-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: #000000;
        background-image: radial-gradient(circle at center, #002244 0%, #000000 70%);
        z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .intro-text {
        font-family: 'Playfair Display', serif; color: #d4af37; font-size: 3rem;
        opacity: 0; animation: fadeIn 1s ease-in forwards 3.5s;
    }
    @keyframes fadeIn { to { opacity: 1; } }

    /* TYPOGRAPHY */
    .big-logo-text { font-family: 'Playfair Display', serif; font-size: 8rem; font-weight: 900; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 4px 4px 10px rgba(0,0,0,0.5); line-height: 1; margin-bottom: 10px; text-align: center; }
    .slogan-text { color: #d4af37; font-size: 1rem; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; margin-bottom: 5px; text-align: center; }
    .vn-slogan-text { color: #fcf6ba; font-size: 1.4rem; letter-spacing: 1px; text-transform: uppercase; font-weight: 900; margin-bottom: 30px; text-align: center; text-shadow: 0 2px 5px rgba(0,0,0,0.3); }
    
    /* FORM & INPUTS */
    .form-container { padding: 30px 40px; background-color: rgba(0, 34, 68, 0.6); border: 1px solid #d4af37; border-radius: 15px; backdrop-filter: blur(10px); }
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div { background-color: #ffffff !important; border: 2px solid #d4af37; color: #000; border-radius: 8px; }
    
    /* BUTTONS */
    .stButton > button { background: linear-gradient(135deg, #b38728 0%, #fbf5b7 50%, #b38728 100%); color: #002244 !important; border: none; font-weight: 800 !important; border-radius: 8px; height: 50px; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: all 0.3s ease; }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px #fcf6ba; }
    
    /* BADGES */
    .status-badge { padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; display: inline-block; margin-right: 10px;}
    .status-pending { background-color: #6c757d; color: white; }
    .status-active { background-color: #0044cc; color: white; }
    .status-resolved { background-color: #00cc66; color: white; }
    .status-disputed { background-color: #cc0000; color: white; }
    .rwa-badge { background-color: #4b0082; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #d4af37; margin-left: 5px; }
    
    /* BANK BOX & TIMELINE */
    .bank-info-box { background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; border: 2px dashed #d4af37; margin-bottom: 20px; }
    .va-number { color: #00ff00; font-family: 'Courier New', monospace; font-size: 1.4rem; font-weight: bold; letter-spacing: 2px; text-shadow: 0 0 10px #00ff00; }
    .timeline-container { display: flex; justify-content: space-around; margin: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
    .timeline-step { text-align: center; font-weight: bold; color: #888; font-size: 0.8rem; flex: 1; }
    .timeline-active { color: #ffca28 !important; text-shadow: 0 0 10px #ffca28; transform: scale(1.1); transition: all 0.3s; }
    
    /* COPYRIGHT FOOTER */
    .copyright-text { text-align: center; color: #888; font-size: 0.7rem; margin-top: 50px; border-top: 1px solid #444; padding-top: 10px; }
    .copyright-highlight { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HÀM KẾT NỐI API NGÂN HÀNG (SEPAY REAL)
# ==========================================
def check_sepay_transaction_real(contract_id, amount_needed):
    """Kiểm tra giao dịch thực tế từ Ngân hàng thông qua SePay API"""
    
    # Kiểm tra xem user đã nhập Token chưa
    if "HAY_DIEN_API" in SEPAY_API_TOKEN:
        time.sleep(1)
        return False, "⚠️ Vui lòng điền SEPAY_API_TOKEN vào code để chạy thật!"

    url = "https://my.sepay.vn/userapi/transactions/list"
    headers = {
        "Authorization": f"Bearer {SEPAY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        with st.spinner(f"🔌 Đang kết nối {MY_BANK_NAME} qua SePay..."):
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('transactions', [])
                
                # Duyệt qua các giao dịch mới nhất
                for trans in transactions:
                    amount_in = float(trans['amount_in'])
                    content = str(trans['transaction_content'])
                    
                    # Logic so khớp: Nội dung chứa Mã HĐ và Tiền >= Yêu cầu
                    if contract_id in content and amount_in >= amount_needed:
                        return True, f"✅ Đã nhận {amount_in:,.0f} VNĐ từ nội dung: {content}"
                
                return False, "⏳ Chưa tìm thấy giao dịch nào khớp lệnh. Vui lòng thử lại sau 1 phút."
            else:
                return False, f"Lỗi kết nối SePay: {response.status_code}"
    except Exception as e:
        return False, f"Lỗi hệ thống: {str(e)}"

# ==========================================
# 4. HỆ THỐNG CƠ SỞ DỮ LIỆU (DATABASE)
# ==========================================
DEFAULT_RWA_BALANCE = 500000000

def hash_password(password): 
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    try: 
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except ValueError: 
        return False

def run_query(query, params=(), fetch_one=False, fetch_all=False):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, params)
        data = None
        if fetch_one: 
            data = c.fetchone()
        elif fetch_all: 
            data = c.fetchall()
        conn.commit()
        conn.close()
        return data
    except sqlite3.Error as e: 
        st.error(f"Lỗi Database: {e}")
        return None

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Bảng User
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password BLOB, rwa_balance REAL DEFAULT 0)''')
    # Bảng Hợp đồng (Đầy đủ cột)
    c.execute('''CREATE TABLE IF NOT EXISTS contracts 
                 (c_id TEXT PRIMARY KEY, 
                 buyer TEXT, seller TEXT, 
                 item_value REAL, total_amount REAL, currency TEXT,
                 description TEXT, status TEXT, created_at TEXT, 
                 accuser TEXT, accuser_reason TEXT, defendant_reason TEXT, delivery_proof TEXT,
                 collateral_type TEXT DEFAULT 'CASH', locked_value REAL DEFAULT 0,
                 virtual_account TEXT)''')
    conn.commit()
    conn.close()

def check_login_secure(username, password):
    user_data = run_query("SELECT password FROM users WHERE username=?", (username,), fetch_one=True)
    if user_data and check_password(password, user_data['password']): 
        return True
    return False

def create_user_secure(username, password):
    existing = run_query("SELECT username FROM users WHERE username=?", (username,), fetch_one=True)
    if existing: 
        return False, "Tên đăng nhập đã tồn tại."
    
    hashed_pw = hash_password(password)
    run_query("INSERT INTO users (username, password, rwa_balance) VALUES (?, ?, ?)", 
              (username, hashed_pw, DEFAULT_RWA_BALANCE))
    return True, "Tạo tài khoản thành công! (Tặng 500tr Token)"

def get_user_rwa(username):
    data = run_query("SELECT rwa_balance FROM users WHERE username=?", (username,), fetch_one=True)
    return data['rwa_balance'] if data else 0

# --- CLASS HỢP ĐỒNG ---
class Contract:
    def __init__(self, c_id, buyer, seller, item_value, total_amount, currency, description, status="PENDING_DEPOSIT", created_at=None, accuser=None, accuser_reason=None, defendant_reason=None, delivery_proof=None, collateral_type="CASH", locked_value=0, virtual_account=None):
        self.c_id = c_id
        self.buyer = buyer
        self.seller = seller
        self.item_value = item_value
        self.total_amount = total_amount
        self.currency = currency
        self.description = description
        self.status = status
        self.created_at = created_at if created_at else datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.accuser = accuser
        self.accuser_reason = accuser_reason
        self.defendant_reason = defendant_reason
        self.delivery_proof = delivery_proof
        self.collateral_type = collateral_type
        self.locked_value = locked_value
        self.virtual_account = virtual_account

    def save_to_db(self):
        run_query("""
            INSERT INTO contracts (c_id, buyer, seller, item_value, total_amount, currency, description, status, created_at, accuser, accuser_reason, defendant_reason, delivery_proof, collateral_type, locked_value, virtual_account)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(c_id) DO UPDATE SET
                status=excluded.status, 
                accuser=excluded.accuser, 
                accuser_reason=excluded.accuser_reason, 
                defendant_reason=excluded.defendant_reason, 
                delivery_proof=excluded.delivery_proof, 
                collateral_type=excluded.collateral_type, 
                locked_value=excluded.locked_value
        """, (self.c_id, self.buyer, self.seller, self.item_value, self.total_amount, self.currency, self.description, self.status, self.created_at, self.accuser, self.accuser_reason, self.defendant_reason, self.delivery_proof, self.collateral_type, self.locked_value, self.virtual_account))

    def auto_approve(self): 
        self.status = "ACTIVE"
        self.save_to_db()

    def lock_rwa(self, username, amount):
        cur = get_user_rwa(username)
        run_query("UPDATE users SET rwa_balance=? WHERE username=?", (cur - amount, username))
        self.status = "ACTIVE"
        self.locked_value = amount
        self.save_to_db()
    
    def seller_confirm_delivery(self, proof): 
        self.delivery_proof = proof
        self.status = "WAITING_CONFIRM"
        self.save_to_db()

    def buyer_confirm_satisfaction(self): 
        self.status = "RESOLVED"
        self.save_to_db()

    def raise_dispute(self, who, reason, proof_file): 
        self.status = "DISPUTED"
        self.accuser = who
        self.accuser_reason = reason
        self.save_to_db()

    def submit_defense(self, reason, proof_file): 
        self.defendant_reason = reason
        self.status = "UNDER_REVIEW"
        self.save_to_db()

    def resolve_dispute_admin(self, winner): 
        self.status = "RESOLVED"
        self.save_to_db()

def load_contracts_from_db(user_role=None, username=None):
    if user_role == 'admin': 
        rows = run_query("SELECT * FROM contracts", fetch_all=True)
    else: 
        rows = run_query("SELECT * FROM contracts WHERE buyer=? OR seller=?", (username, username), fetch_all=True)
    
    contracts = []
    if rows:
        for row in rows: 
            contracts.append(Contract(row['c_id'], row['buyer'], row['seller'], row['item_value'], row['total_amount'], row['currency'], row['description'], row['status'], row['created_at'], row['accuser'], row['accuser_reason'], row['defendant_reason'], row['delivery_proof'], row['collateral_type'], row['locked_value'], row['virtual_account']))
    return contracts

# --- SESSION STATE ---
if 'logged_in_user' not in st.session_state: st.session_state['logged_in_user'] = None
if 'view_mode' not in st.session_state: st.session_state['view_mode'] = 'login'
if 'intro_shown' not in st.session_state: st.session_state['intro_shown'] = False

# ==========================================
# 5. GIAO DIỆN CHÍNH
# ==========================================
def login_page():
    c_logo, c_form = st.columns([1, 2])
    with c_logo: 
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Sử dụng icon xoay 3D
        st.markdown(f'<img src="{icon_url}" class="rotating-logo" width="250">', unsafe_allow_html=True)
    
    with c_form:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="big-logo-text">3 L H</h1>', unsafe_allow_html=True)
        st.markdown('<p class="slogan-text">TRIPLE LAYER HONOR - REAL BANKING</p>', unsafe_allow_html=True)
        st.markdown('<p class="vn-slogan-text">BẢO CHỨNG NIỀM TIN SỐ</p>', unsafe_allow_html=True)
        
        if st.session_state['view_mode'] == 'login':
            with st.form("login_form"):
                u = st.text_input("Tài khoản")
                p = st.text_input("Mật khẩu", type="password")
                if st.form_submit_button("TRUY CẬP HỆ THỐNG", use_container_width=True):
                    if check_login_secure(u, p): 
                        st.session_state['logged_in_user'] = u
                        st.rerun()
                    else: 
                        st.error("Sai thông tin.")
            st.markdown("---")
            if st.button("ĐĂNG KÝ NGAY"): 
                st.session_state['view_mode'] = 'reg'
                st.rerun()
        
        elif st.session_state['view_mode'] == 'reg':
            st.markdown("### ĐĂNG KÝ MỚI")
            with st.form("reg_form"):
                nu = st.text_input("Tên đăng nhập")
                np = st.text_input("Mật khẩu", type="password")
                if st.form_submit_button("ĐĂNG KÝ"):
                    if nu and np:
                        suc, msg = create_user_secure(nu, np)
                        if suc: 
                            st.success(msg)
                            time.sleep(1.5)
                            st.session_state['view_mode'] = 'login'
                            st.rerun()
                        else: 
                            st.warning(msg)
            if st.button("Quay lại"): 
                st.session_state['view_mode'] = 'login'
                st.rerun()
        
        # --- BẢN QUYỀN (FOOTER) ---
        st.markdown("<div class='copyright-text'>© 2026 3LH GLOBAL ESCROW. DEVELOPED BY <span class='copyright-highlight'>VƯƠNG LUÂN</span>. ALL RIGHTS RESERVED.</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard():
    user = st.session_state['logged_in_user']
    user_rwa = get_user_rwa(user)
    
    with st.sidebar:
        # --- LOGO BÀN LÀM VIỆC ---
        st.markdown(f'<img src="{icon_url}" class="rotating-logo" width="150" style="display:block; margin:auto; margin-bottom: 20px;">', unsafe_allow_html=True)
        st.markdown(f"### Xin chào, {user}")
        st.caption(f"💎 RWA Balance: {user_rwa:,.0f}")
        st.markdown("---")
        if st.button("ĐĂNG XUẤT", use_container_width=True): 
            st.session_state['logged_in_user'] = None
            st.rerun()
        
        # --- BẢN QUYỀN (SIDEBAR) ---
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='copyright-text'>© 2026 3LH INC.<br>Created by <b style='color:#d4af37'>VƯƠNG LUÂN</b></div>", unsafe_allow_html=True)

    st.markdown(f"## 🛡️ BÀN LÀM VIỆC ĐIỀU HÀNH")
    tabs = ["TẠO GIAO DỊCH MỚI", "QUẢN LÝ TÀI SẢN"]
    if user == "admin": 
        tabs.append("TÒA ÁN SỐ")
        tabs.append("DUYỆT KÝ QUỸ")
    
    active_tab = st.tabs(tabs)

    # --- TAB 1: TẠO HỢP ĐỒNG ---
    with active_tab[0]:
        with st.form("new_c_form"):
            st.markdown("#### 1. Thông tin giao dịch"); st.markdown("---")
            col_buyer, col_seller = st.columns(2, gap="medium")
            with col_buyer:
                st.markdown("##### 🟦 Bên Mua (Bạn)")
                st.text_input("Tài khoản", value=user, disabled=True)
            with col_seller:
                st.markdown("##### 🟧 Bên Bán (Đối tác)")
                partner = st.text_input("Tài khoản đối tác")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 💰 Thiết lập thanh toán")
            c_cur, c_item, c_dep = st.columns([1, 2, 2])
            with c_cur: 
                currency = st.selectbox("Loại tiền", ["VNĐ"]) 
            with c_item: 
                item_val = st.number_input(f"Giá trị hàng", min_value=0.0, step=10000.0, format="%d")
            with c_dep:
                deposit_val = st.number_input(f"Số tiền Ký quỹ", min_value=0.0, step=10000.0, format="%d")
                if deposit_val < item_val: 
                    st.error("⚠️ Tiền Ký quỹ phải LỚN HƠN hoặc BẰNG Giá trị hàng!")
            st.caption(f"*Lưu ý: Bạn cần nạp đủ **{deposit_val:,.0f} VNĐ**.*")
            
            desc = st.text_area("Nội dung giao dịch chi tiết", height=80)
            
            st.markdown("---")
            st.caption("Tùy chọn nâng cao (Risk Management):")
            method = st.radio("Phương thức bảo đảm:", ["Tiền mặt (Standard)", "RWA Token (Overcollateralized - 150%)"], horizontal=True)
            
            submitted = st.form_submit_button("KHỞI TẠO HỢP ĐỒNG", use_container_width=True)
            
            if submitted:
                if partner and item_val > 0 and deposit_val > 0:
                    if deposit_val < item_val: 
                        st.error("Không thể tạo: Tiền Ký quỹ thấp hơn Giá trị hàng.")
                    else:
                        if "RWA" in method:
                             req_token = deposit_val * 1.5
                             if user_rwa >= req_token:
                                 count_data = run_query("SELECT COUNT(*) FROM contracts", fetch_one=True)
                                 new_id = f"RWA-{count_data[0]+1:03d}"
                                 nc = Contract(new_id, user, partner, item_val, deposit_val, currency, desc, collateral_type="RWA", locked_value=req_token, virtual_account="N/A")
                                 nc.lock_rwa(user, req_token)
                                 st.success(f"Đã tạo HĐ RWA."); time.sleep(1.5); st.rerun()
                             else: 
                                 st.error(f"Thiếu Token RWA. Cần: {req_token:,.0f}")
                        else:
                            count_data = run_query("SELECT COUNT(*) FROM contracts", fetch_one=True)
                            next_id = count_data[0] + 1
                            new_id = f"HD-{next_id:03d}"
                            nc = Contract(new_id, user, partner, item_val, deposit_val, currency, desc, collateral_type="CASH", virtual_account="N/A")
                            nc.save_to_db()
                            st.success("Hợp đồng đã tạo thành công!"); time.sleep(1.5); st.rerun()
                else: 
                    st.warning("Vui lòng nhập đủ thông tin.")

        # --- KHÔI PHỤC HIẾN PHÁP (QUY TẮC) ---
        with st.expander("📜 Xem chi tiết: QUY TẮC VẬN HÀNH & GIẢI QUYẾT TRANH CHẤP"):
            st.markdown("""
            **1. QUY ĐỊNH VỀ PHÍ & THỜI GIAN**
            * **Phí dịch vụ:** Không hoàn lại dù giao dịch thành công hay thất bại.
            * **Thời gian xử lý Ký quỹ:** Tối đa 30 phút (Giờ hành chính).
            
            **2. NGUYÊN TẮC BẢO VỆ**
            * 3LH chỉ giữ tiền, **KHÔNG** giữ hàng.
            * Giải ngân ngay khi Người Mua xác nhận **HOẶC** sau 24h kể từ khi Người Bán báo giao hàng.
            
            **3. LUẬT GIẢI QUYẾT TRANH CHẤP**
            * **Giai đoạn 1 (12h đầu):** Hai bên tự thương lượng.
            * **Giai đoạn 2 (Sau 12h):** Admin 3LH phán xử dựa trên **Bằng chứng (Proof)**.
            * **Lưu ý:** Bên nào làm giả bằng chứng sẽ bị khóa tài khoản vĩnh viễn.
            """)

    # --- TAB 2: QUẢN LÝ TÀI SẢN ---
    with active_tab[1]:
        my_contracts = load_contracts_from_db(username=user)
        if not my_contracts: st.info("Chưa có giao dịch nào.")
        
        # SỬ DỤNG CONTAINER CUỘN DỌC
        with st.container(height=600, border=True):
            for c in my_contracts:
                badge_html = ""; timeline_html = ""
                if c.status == "PENDING_DEPOSIT":
                    badge_html = "<span class='status-badge status-pending'>⏳ Chờ Ký Quỹ</span>"
                    timeline_html = """<div class='timeline-container'><div class='timeline-step timeline-active'>1. Chờ Ký Quỹ<br>🔄</div><div class='timeline-step'>2. Đang Thực Hiện<br>⏳</div><div class='timeline-step'>3. Chờ Xác Nhận<br>⏳</div><div class='timeline-step'>4. Hoàn Tất<br>🏁</div></div>"""
                elif c.status == "ACTIVE":
                    badge_html = "<span class='status-badge status-active'>🔵 Đang Thực Hiện</span>"
                    timeline_html = """<div class='timeline-container'><div class='timeline-step timeline-active'>1. Đã Ký Quỹ<br>✅</div><div class='timeline-step timeline-active'>2. Đang Thực Hiện<br>🔄</div><div class='timeline-step'>3. Chờ Xác Nhận<br>⏳</div><div class='timeline-step'>4. Hoàn Tất<br>🏁</div></div>"""
                elif c.status == "WAITING_CONFIRM":
                    badge_html = "<span class='status-badge status-waiting'>🟡 Chờ Xác Nhận</span>"
                    timeline_html = """<div class='timeline-container'><div class='timeline-step timeline-active'>1. Đã Ký Quỹ<br>✅</div><div class='timeline-step timeline-active'>2. Đang Thực Hiện<br>✅</div><div class='timeline-step timeline-active'>3. Chờ Xác Nhận<br>🔄</div><div class='timeline-step'>4. Hoàn Tất<br>⏳</div></div>"""
                elif c.status == "RESOLVED": 
                    badge_html = "<span class='status-badge status-resolved'>🟢 Hoàn Tất</span>"
                elif c.status in ["DISPUTED", "UNDER_REVIEW"]: 
                    badge_html = "<span class='status-badge status-disputed'>🔴 Tranh Chấp</span>"
                
                if c.collateral_type == "RWA": badge_html += "<span class='rwa-badge'>🔒 RWA Secured</span>"
                amt_display = f"{c.total_amount:,.0f} {c.currency}"

                with st.expander(f"{c.c_id} | {amt_display} | {c.description}"):
                    st.markdown(badge_html, unsafe_allow_html=True)
                    if timeline_html: st.markdown(timeline_html, unsafe_allow_html=True)
                    st.markdown("---")
                    
                    if c.status == "PENDING_DEPOSIT" and c.collateral_type == "CASH":
                        if user == c.buyer:
                             st.markdown(f"""
                             <div class='bank-info-box'>
                                 <h4 style='color: #d4af37; text-align: center;'>⚠️ QUÉT MÃ ĐỂ KÝ QUỸ</h4>
                                 <p style='text-align: center;'>Vui lòng chuyển <b>{amt_display}</b> tới:</p>
                                 <hr style='border-color: #d4af37;'>
                                 <p><b>🏦 Ngân hàng:</b> {MY_BANK_NAME}</p>
                                 <p><b>💳 Số tài khoản:</b> <span style='font-size: 1.2rem; font-weight: bold; color: #ffca28;'>{MY_BANK_ACCOUNT}</span></p>
                                 <p style='text-align: center;'>📝 Nội dung chuyển khoản (BẮT BUỘC):</p>
                                 <p style='text-align: center;'><span class='va-number'>{c.c_id}</span></p>
                             </div>
                             """, unsafe_allow_html=True)
                             
                             col_api, col_desc = st.columns([1,2])
                             with col_api:
                                 if st.button("🔄 KIỂM TRA (SEPAY)", key=f"api_{c.c_id}"):
                                     suc, msg = check_sepay_transaction_real(c.c_id, c.total_amount)
                                     if suc: 
                                         c.auto_approve()
                                         st.success(msg)
                                         time.sleep(2)
                                         st.rerun()
                                     else:
                                         st.warning(msg)
                             with col_desc: st.caption(f"Hệ thống đang kết nối Ngân hàng thực tế để tìm nội dung '{c.c_id}'...")
                        else: 
                            st.info("⏳ Đang chờ Bên Mua thực hiện ký quỹ.")
                    
                    elif c.status == "ACTIVE":
                        if user == c.seller:
                            with st.form(f"delivery_{c.c_id}"):
                                proof_desc = st.text_area("Nhập bằng chứng giao hàng", height=70)
                                if st.form_submit_button("📦 BÁO CÁO ĐÃ GIAO HÀNG"): 
                                    c.seller_confirm_delivery(proof_desc)
                                    st.rerun()
                        else: 
                            st.info("👉 Tiền đang được bảo vệ. Vui lòng chờ đối tác giao hàng.")
                    
                    elif c.status == "WAITING_CONFIRM":
                        if user == c.buyer:
                             st.warning("👉 Đối tác đã báo cáo giao hàng. Vui lòng kiểm tra."); st.markdown(f"**Bằng chứng:** {c.delivery_proof}")
                             c1, c2 = st.columns([2, 1])
                             with c1: 
                                 if st.button("✅ XÁC NHẬN HÀI LÒNG", key=f"btn_ok_{c.c_id}", type="primary"): 
                                     c.buyer_confirm_satisfaction()
                                     st.rerun()
                             with c2: 
                                 with st.popover("🚨 BÁO CÁO VẤN ĐỀ"):
                                     reason = st.text_area("Lý do")
                                     if st.button("GỬI KHIẾU NẠI"): 
                                         c.raise_dispute(user, reason, None)
                                         st.rerun()
                        else: 
                            st.info("👉 Đã báo cáo. Chờ Bên Mua xác nhận.")
                    
                    elif c.status == "RESOLVED": 
                        st.success("✅ Giao dịch hoàn tất.")
                    
                    elif c.status in ["DISPUTED", "UNDER_REVIEW"]:
                         st.error(f"ĐANG TRANH CHẤP TẠI TÒA ÁN. Trạng thái: {c.status}")
                         if user != c.accuser and user != 'admin' and c.status == "DISPUTED":
                             with st.form(f"def_{c.c_id}"):
                                 dr = st.text_area("Lời giải trình")
                                 if st.form_submit_button("GỬI GIẢI TRÌNH"):
                                     c.submit_defense(dr, None)
                                     st.rerun()

    # --- TAB 3: ADMIN ---
    if user == "admin" and len(tabs) > 2:
        with active_tab[2]:
            st.markdown("### ⚖️ PHÒNG XỬ ÁN (ADMIN)")
            with st.container(height=600, border=True):
                all_c = load_contracts_from_db(user_role='admin')
                review_c = [c for c in all_c if c.status == "UNDER_REVIEW"]
                if not review_c: 
                    st.success("Không có vụ án chờ xét xử.")
                for rc in review_c:
                    with st.expander(f"Vụ án: {rc.c_id}", expanded=True):
                        st.write(f"Bằng chứng: {rc.delivery_proof}")
                        c_acc, c_def = st.columns(2)
                        c_acc.info(f"Nguyên đơn ({rc.accuser}): {rc.accuser_reason}")
                        c_def.error(f"Bị đơn: {rc.defendant_reason}")
                        winner = st.radio("Phán quyết thắng:", [rc.buyer, rc.seller], key=rc.c_id)
                        if st.button("🔨 TUYÊN ÁN", key=f"btn_{rc.c_id}"):
                            rc.resolve_dispute_admin(winner)
                            st.rerun()

    if user == "admin" and len(tabs) > 3:
        with active_tab[3]:
            st.markdown("### 💰 DUYỆT KÝ QUỸ THỦ CÔNG")
            with st.container(height=600, border=True):
                all_c = load_contracts_from_db(user_role='admin')
                pending_c = [c for c in all_c if c.status == "PENDING_DEPOSIT" and c.collateral_type=="CASH"]
                if not pending_c: 
                    st.success("Không có khoản chờ duyệt.")
                for pc in pending_c:
                    with st.expander(f"⏳ {pc.c_id} | {pc.total_amount:,.0f} {pc.currency}"):
                        st.write(f"Nội dung: KQ {pc.c_id}")
                        if st.button(f"✅ XÁC NHẬN ĐÃ NHẬN TIỀN", key=f"btn_approve_{pc.c_id}"):
                            pc.auto_approve()
                            st.rerun()

if __name__ == "__main__":
    if not os.path.exists(DB_NAME): init_db()
    if not st.session_state['intro_shown']:
        st.markdown("""<div class='intro-container'><img src='"""+icon_url+"""' class='intro-spinning-logo'><div class='intro-text'>BẢO CHỨNG NIỀM TIN SỐ</div></div>""", unsafe_allow_html=True)
        time.sleep(5); st.session_state['intro_shown'] = True; st.rerun()
    else:
        if st.session_state['logged_in_user']: dashboard()
        else: login_page()