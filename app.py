import streamlit as st
import requests
import json
import uuid
import base64

# 👉 KHỞI TẠO SESSION STATE nếu chưa có
if "cart" not in st.session_state:
    st.session_state.cart = []

if "view_cart" not in st.session_state:
    st.session_state.view_cart = False

from datetime import datetime

# CSS
st.markdown("""
<style>
.product-name {
    font-weight: bold;
    text-align: center;
    margin-top: 10px;
}
.product-price {
    color: blue;
    margin-top: 5px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# Danh sách sản phẩm
fruit_products = [
    {"name": "Bơ 034", "price": 35000, "image": "034.jpg"},
    {"name": "Bơ Booth", "price": 30000, "image": "booth.jpg"},
    {"name": "Bơ sáp Nhật", "price": 30000, "image": "sap_nhat.jpg"},
    {"name": "Sầu riêng Ri6", "price": 80000, "image": "ri6.jpg"},
    {"name": "Sầu riêng Dona", "price": 85000, "image": "dona.jpg"},
    {"name": "Sầu riêng MusangKing", "price": 110000, "image": "musangking.jpg"},
]


nut_products = [
    {"name": "Macca sấy size đại", "price": 230000, "image": "macca_lon.jpg"},
    {"name": "Macca sấy size trung", "price": 210000, "image": "macca_nho.jpg"},
    {"name": "Hạt điều rang tách vỏ lụa", "price": 370000, "image": "dieutachvo.jpg"},
    {"name": "Bột ngũ cốc", "price": 200000, "image": "botngucoc.jpg"},
    {"name": "Hạt điều rang muối", "price": 210000, "image": "hatdieu.jpg"},
    {"name": "Granola", "price": 150000, "image": "granola.jpg"},
]

# Danh sách hết hàng
trai_het = ["Bơ 034", "Bơ Booth", "Bơ sáp Nhật", "Sầu riêng Ri6", "Sầu riêng Dona"]
hat_het = ["Hạt điều rang muối", "Granola",  "Macca sấy size trung"]

# Gắn cờ hết hàng
for item in fruit_products:
    item["het_hang"] = item["name"] in trai_het

for item in nut_products:
    item["het_hang"] = item["name"] in hat_het




def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64_of_bin_file("avo8.jpg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.9;
    }}

    h1 {{
        text-align: center;
        font-size: 50px;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Nông sản Đăk Lăk</h1>", unsafe_allow_html=True)


# st.title("Nông sản Đăk Lăk")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        width: 33.33%;
        padding: 20px 0;
        font-size: 20px;
        font-weight: bold;
        background-color: #f0f0f0;
        border-radius: 10px 10px 0 0;
        margin-right: 5px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e0e0;
        cursor: pointer;
    }
    .stTabs [aria-selected="true"] {
        background-color: #d9f0ff !important;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Sản phẩm Quả", "Sản phẩm Hạt", "Về Cửa hàng"])

with tab1:
    st.subheader("Danh sách Quả")
    for i in range(0, len(fruit_products), 3):
        cols = st.columns(3)
        for col, p in zip(cols, fruit_products[i:i+3]):
            with col:
                st.image(p["image"], use_container_width=True)
                st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-price'>Giá: {p['price']:,} đ / kg</div>", unsafe_allow_html=True)
                if p.get("het_hang", False):
                    st.markdown(" <span style='color:red'>Đã hết hàng</span>", unsafe_allow_html=True)
                else:
                    qty = st.number_input(f"Số ký - {p['name']}", min_value=1, max_value=100, value=1, key=f"qty_{p['name']}")
                    if st.button(f"🛒 Thêm - {p['name']}", key=f"btn_{p['name']}"):
                        st.session_state.cart.append({
                            "name": p["name"],
                            "price": p["price"],
                            "quantity": qty
                        })
                        st.success(f"✅ Đã thêm {qty} kg {p['name']} vào giỏ hàng!")

with tab2:
    st.subheader("Danh sách Hạt")
    for i in range(0, len(nut_products), 3):
        cols = st.columns(3)
        for col, p in zip(cols, nut_products[i:i+3]):
            with col:
                st.image(p["image"], use_container_width=True)
                st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-price'>Giá: {p['price']:,} đ / kg</div>", unsafe_allow_html=True)
                if p.get("het_hang", False):
                    st.markdown(" <span style='color:red'>Đã hết hàng</span>", unsafe_allow_html=True)
                else:
                    qty = st.number_input(f"Số ký - {p['name']}", min_value=0.5, max_value=100.0, value=1.0, step=0.5, key=f"qty_{p['name']}")
                    if st.button(f"🛒 Thêm - {p['name']}", key=f"btn_{p['name']}"):
                        st.session_state.cart.append({
                            "name": p["name"],
                            "price": p["price"],
                            "quantity": qty
                        })
                        st.success(f"✅ Đã thêm {qty} kg {p['name']} vào giỏ hàng!")


            st.markdown('</div>', unsafe_allow_html=True)



with st.expander("🛒 Xem giỏ hàng", expanded=False):
    st.write("### 🧾 Giỏ hàng của bạn:")
    if st.session_state.cart:
        total = 0
        cart_items_to_remove = []  # Danh sách index sản phẩm cần xoá

        for i, item in enumerate(st.session_state.cart):
            item_total = item["price"] * item["quantity"]
            st.write(f"- {item['name']}: {item['quantity']} kg x {item['price']:,} đ = {item_total:,} đ")

            # Nút xoá sản phẩm
            if st.button(f"❌ Xoá {item['name']}", key=f"remove_{i}"):
                cart_items_to_remove.append(i)

            total += item_total

        # Xoá các sản phẩm cần xoá
        if cart_items_to_remove:
            for i in sorted(cart_items_to_remove, reverse=True):
                del st.session_state.cart[i]
            st.rerun()  # Refresh lại app

        st.write(f"**Tổng cộng: {total:,} đ**")

    else:
        st.info("Giỏ hàng của bạn đang trống.")



# Hiển thị form thu thập thông tin khách hàng sau khi xem giỏ hàng
if "cart" in st.session_state and st.session_state.cart:
    with st.form("customer_info_form"):
        st.markdown("### 📋 Thông tin khách hàng")
        customer_name = st.text_input("👤 Họ và tên", placeholder="Nhập tên đầy đủ của bạn")
        phone = st.text_input("📱 Số điện thoại", placeholder="Ví dụ: 0909123456")
        address = st.text_area("🏠 Địa chỉ giao hàng", placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành")
        note = st.text_area("📝 Ghi chú thêm", placeholder="(Không bắt buộc)")
        payment_method = st.radio(
            "💳 Hình thức thanh toán",
            ("Chuyển khoản trực tiếp", "Thanh toán khi nhận hàng (COD)"),
            index=0
            )
        
        submit = st.form_submit_button("✅ Xác nhận đặt hàng")
        if submit:
            if not customer_name or not phone or not address:
                st.error("❗ Vui lòng điền đầy đủ thông tin bắt buộc.")
            else:
                if payment_method == "Chuyển khoản trực tiếp":
                    st.markdown("**👉 Vui lòng chuyển khoản đến thông tin sau, nội dung chuyển khoản là SỐ ĐIỆN THOẠI ĐẶT HÀNG:**")
                    st.markdown("- Ngân hàng: BIDV")
                    st.markdown("- Số tài khoản: 1680001755")
                    st.markdown("- Chủ tài khoản: Trần Hà Tường Vi")
                    # Hiển thị mã QR ngân hàng
                    st.image("qr_bank.jpg", caption="Quét để chuyển khoản", width=300)

                st.success("Cảm ơn bạn đã mua hàng. Bạn vui lòng chờ trong giây lát")

                # 👉 TẠO order_id duy nhất cho đơn hàng
                order_id = str(uuid.uuid4())[:5]  # Lấy 5 ký tự đầu để dễ nhìn

                # 👉 Tính tổng tiền đơn hàng
                order_total_amount = sum(item["price"] * item["quantity"] for item in st.session_state.cart)

                # Gửi đơn hàng về Google Sheets TRƯỚC khi xóa giỏ hàng
                order_data = [{
                    "order_id": order_id,
                    "name": customer_name,
                    "phone": phone,
                    "address": address,
                    "note": note,
                    "product": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "total": item["price"] * item["quantity"],
                    "order_total": order_total_amount,
                    "payment_method": payment_method
                    
                } for item in st.session_state.cart]

                # Gửi dữ liệu đến webhook Google Apps Script
                webhook_url = "https://script.google.com/macros/s/AKfycbzSV-4E7NImctVlaHBFFtBSDiZVoqWD3IDLZ2Hw2LzwOyi09YtM0phfe9BDxBR051SuWQ/exec"  # Thay bằng link của bạn
                response = requests.post(webhook_url, data=json.dumps(order_data))

                if response.status_code == 200:
                    st.success("Đặt hàng thành công!")
                else:
                    st.error(f"❌ Gửi đơn hàng thất bại. Mã lỗi: {response.status_code}")

                # Hiển thị đơn hàng tóm tắt
                st.write("### 🧾 Thông tin đơn hàng:")
                total = 0
                for item in st.session_state.cart:
                    item_total = item["price"] * item["quantity"]
                    st.write(f"- {item['name']}: {item['quantity']} kg x {item['price']:,} đ = {item_total:,} đ")
                    total += item_total
                st.write(f"**Tổng cộng: {total:,} đ**")

                # Hiển thị thông tin khách hàng
                st.write("### 👤 Thông tin Khách hàng:")
                st.write(f"- Họ tên: {customer_name}")
                st.write(f"- Số điện thoại: {phone}")
                st.write(f"- Địa chỉ: {address}")
                if note:
                    st.write(f"- Ghi chú: {note}")
 

 
with tab3:
    st.subheader("🏪 Về cửa hàng Nông sản Đăk Lăk")
    st.image("macatree.jpg", use_container_width=True)
    st.markdown("""
    **Chào mừng bạn đến với Cửa hàng Nông sản Đăk Lăk!**

    🍃 Từ những vùng đất màu mỡ của Tây Nguyên, chúng tôi mang đến các loại trái cây tươi ngon, theo đúng mùa, được tuyển chọn từ vườn nhà của những người bà con thân quen. 
                Do đó các loại trái cây này là những loại trái đang chính vụ và có thể các sản phẩm sẽ hết trước khi mùa vụ kết thúc.
                Đối với hạt, đây là một trong những sản phẩm ngon được tuyển chọn kỹ lưỡng về mùi vị tại Buôn Hồ, xứ xở của mắc ca để đảm bảo chất lượng luôn tươi mới mỗi mùa.
                 

    ✅ Cam kết:
    - Nông sản sạch – chính vụ, không chất bảo quản.
    - Giao hàng toàn quốc.
    - Hỗ trợ đổi trả.
    - Giao hàng trong vòng 1-3 ngày (tùy từng đợt hàng).
    

    📞 Liên hệ: **0989 29 26 54** (zalo)
    """)







