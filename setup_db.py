import sqlite3

# Tên file cơ sở dữ liệu (Cuốn sổ cái của chúng ta)
DB_NAME = "3lh_ledger.db"

def init_db():
    """Hàm này sẽ tạo ra file database và các bảng trống nếu chưa có"""
    print(f"🔄 Đang khởi tạo Sổ cái 3LH ({DB_NAME})...")
    
    # 1. Kết nối (Nếu file chưa có, nó sẽ tự tạo mới)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 2. Tạo Bảng USER (Thành viên)
    # Cú pháp SQL: Tạo bảng nếu chưa tồn tại, cột username là khóa chính (không trùng)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # 3. Tạo Bảng CONTRACTS (Hợp đồng & Tranh chấp)
    # Lưu trữ các trường thông tin cốt lõi
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
    
    # 4. Tạo dữ liệu mẫu ban đầu (Admin & User gốc) để test
    # Dùng INSERT OR IGNORE để nếu chạy lại nhiều lần không bị lỗi trùng lặp
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123')")
    c.execute("INSERT OR IGNORE INTO users VALUES ('Luan_VN', '1985')")
    c.execute("INSERT OR IGNORE INTO users VALUES ('Doi_tac_A', '123')")

    # 5. Lưu lại và đóng kết nối
    conn.commit()
    conn.close()
    print("✅ Đã khởi tạo thành công! File '3lh_ledger.db' đã sẵn sàng.")

# Chạy hàm khởi tạo
if __name__ == "__main__":
    init_db()