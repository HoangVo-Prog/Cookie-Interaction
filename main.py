from utils import setup_driver
import json
import time


driver = setup_driver()

# url = "https://chatgpt.com/"
url = "https://notebooklm.google.com/"
driver.get(url)
time.sleep(2)

with open("notebook_cookie.json", "r") as f:
    cookies = json.load(f)

print("Trang hiện tại:", driver.current_url)



# === Thêm từng cookie vào trình duyệt ===
for cookie in cookies:
    # Bỏ qua cookie nếu có field không được Selenium hỗ trợ
    cookie_dict = {
        "name": cookie.get("name"),
        "value": cookie.get("value"),
        "path": cookie.get("path", "/")
    }

    # Chỉ thêm domain nếu KHỚP với domain hiện tại
    if "domain" in cookie and cookie["domain"] in driver.current_url:
        cookie_dict["domain"] = cookie["domain"]

    # Nếu có 'expiry', đảm bảo là số nguyên
    if "expirationDate" in cookie:
        cookie_dict["expiry"] = int(cookie["expirationDate"])

    try:
        driver.add_cookie(cookie_dict)
    except Exception as e:
        print(f"[❌] Không thêm được cookie: {cookie_dict['name']} - {e}")


# === Tải lại trang để áp dụng cookie ===
driver.get(url)
time.sleep(5)

# === Quan sát xem đã login chưa ===
input("Đã load cookie. Nhấn Enter để thoát...")
driver.save_screenshot("screenshot.png")
driver.quit()

