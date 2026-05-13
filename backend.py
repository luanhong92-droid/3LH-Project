from flask import Flask, render_template

app = Flask(__name__)

# Dữ liệu mô phỏng từ hình ảnh anh gửi
PRODUCTS = [
    {
        "id": 1,
        "name": "Mô tơ cổng mở tự động cánh tay đòn C04 Swing...",
        "price": "6.888.000đ",
        "old_price": "8.400.000đ",
        "discount": "-18%",
        "rating": "5.0",
        "sold": "3",
        "image": "https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-ljv7n5p5x5m96a", # Link ảnh minh họa
        "aff_link": "https://shope.ee/link_cua_anh_1"
    },
    {
        "id": 2,
        "name": "Biến tần 3 trong 1 CPE 24V3000W (Biến tần xung)",
        "price": "5.330.000đ",
        "old_price": "6.500.000đ",
        "discount": "-18%",
        "rating": "4.8",
        "sold": "20",
        "image": "https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-ljv7n5p5x5m96b",
        "aff_link": "https://shope.ee/link_cua_anh_2"
    },
    {
        "id": 3,
        "name": "Xi lanh điện tự động 24V YNT hành trình 100mm-500mm",
        "price": "817.800đ",
        "old_price": "1.000.000đ",
        "discount": "-20%",
        "rating": "4.9",
        "sold": "105",
        "image": "https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-ljv7n5p5x5m96c",
        "aff_link": "https://shope.ee/link_cua_anh_3"
    },
    {
        "id": 4,
        "name": "Remote cổng xếp Bai Sheng",
        "price": "150.000đ",
        "old_price": "200.000đ",
        "discount": "-25%",
        "rating": "5.0",
        "sold": "500",
        "image": "https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-ljv7n5p5x5m96d",
        "aff_link": "https://shope.ee/link_cua_anh_4"
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)