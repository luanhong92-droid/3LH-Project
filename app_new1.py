import streamlit as st
import feedparser
from bs4 import BeautifulSoup

# --- 1. CẤU HÌNH GIAO DIỆN RỘNG (WIDE) ---
# Bắt buộc dùng wide để có không gian dàn 3 cột giống giao diện anh yêu cầu
st.set_page_config(page_title="Tin Tức Trực Quan", page_icon="📰", layout="wide")

st.markdown("### 📰 TIN MỚI NHẤT")
st.divider()

# --- 2. XỬ LÝ DỮ LIỆU & BÓC TÁCH HÌNH ẢNH ---
RSS_URL = "https://vnexpress.net/rss/tin-moi-nhat.rss"

@st.cache_data(ttl=600) # Cập nhật sau 10 phút
def fetch_news_with_images():
    feed = feedparser.parse(RSS_URL)
    news_items = []
    
    # Lấy 15 bài viết mới nhất để chia đều cho 3 cột
    for entry in feed.entries[:15]: 
        # VNExpress giấu link ảnh trong thẻ <description>, cần dùng BeautifulSoup để bóc tách
        soup = BeautifulSoup(entry.description, 'html.parser')
        img_tag = soup.find('img')
        
        # Nếu bài không có ảnh, dùng ảnh mặc định chống lỗi giao diện
        img_url = img_tag['src'] if img_tag else "https://via.placeholder.com/500x300?text=No+Image"
        
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "image": img_url,
            "date": entry.published
        })
    return news_items

news_data = fetch_news_with_images()

# --- 3. DÀN TRANG DẠNG LƯỚI (GRID LAYOUT) ---
if not news_data:
    st.error("Không thể kết nối nguồn tin.")
else:
    # Chia giao diện thành 3 cột bằng nhau
    cols = st.columns(3)
    
    # Vòng lặp phân bổ từng bản tin vào lần lượt cột 1, cột 2, cột 3
    for index, item in enumerate(news_data):
        with cols[index % 3]:
            # st.container giúp gom nhóm ảnh và chữ thành 1 khối (Card)
            with st.container(border=True):
                # Hiển thị ảnh bìa, tự động co giãn vừa chiều rộng cột
                st.image(item["image"], use_container_width=True)
                
                # Hiển thị Tiêu đề (in đậm, có gắn link) và Thời gian
                st.markdown(f"**[{item['title']}]({item['link']})**")
                st.caption(f"🕒 {item['date']}")
                
                # Nút đọc tương tác mượt mà hơn
                st.link_button("Xem chi tiết", item['link'], use_container_width=True)