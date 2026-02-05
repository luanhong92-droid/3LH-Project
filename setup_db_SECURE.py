# --- FILE: setup_db_SECURE.py (Phiên bản bảo mật) ---
import sqlite3
import bcrypt  # <--- Thư viện bảo mật mới

DB_NAME = "3lh_ledger.db"

def hash_password(password):
    """Hàm biến mật khẩu thô thành chuỗi mã hóa không thể dịch ngược"""
    # Tạo 'muối' (salt) ngẫu nhiên và băm mật khẩu
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed # Trả về dạng bytes

def init_db_secure():
    print(f"🔄 Đang khởi tạo Sổ cái BẢO MẬT 3LH ({DB_NAME})...")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Bảng users giờ đây lưu password dưới dạng BLOB (Dữ liệu nhị phân) thay vì TEXT
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password BLOB NOT NULL 
        )
    ''')
    
    # Bảng contracts giữ nguyên
    c.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            c_id TEXT PRIMARY KEY,
            buyer TEXT NOT NULL,
            seller TEXT NOT NULL,
            total_amount REAL NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT,
            accuser TEXT,
            accuser_reason TEXT,
            defendant_reason TEXT
        )
    ''')

    # --- TẠO DỮ LIỆU MẪU ĐÃ ĐƯỢC MÃ HÓA ---
    users_to_add = [
        ('admin', 'admin123'),
        ('Luan_VN', '1985'),
        ('Doi_tac_A', '123')
    ]

    print("🔒 Đang mã hóa mật khẩu và lưu trữ...")
    for u, p_raw in users_to_add:
        # Băm mật khẩu trước khi lưu
        p_hashed = hash_password(p_raw)
        try:
            c.execute("INSERT INTO users VALUES (?, ?)", (u, p_hashed))
        except sqlite3.IntegrityError:
            pass # Bỏ qua nếu đã tồn tại

    conn.commit()
    conn.close()
    print("✅ Đã khởi tạo thành công Sổ cái BẢO MẬT! Mọi mật khẩu đã được băm.")

if __name__ == "__main__":
    init_db_secure()