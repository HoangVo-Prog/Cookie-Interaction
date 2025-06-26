from utils import setup_driver, perform_login
import json
import time

driver = setup_driver()

def save_cookie(driver):
    driver.get("https://accounts.google.com/")

    perform_login(driver, "vh22042204@gmail.com", "Helloworld@123")

    input()
    cookies = driver.get_cookies()

    with open("google_cookies.json", "w") as f:
        json.dump(cookies, f)

# save_cookie(driver)

driver.get("https://www.google.com")
time.sleep(2)

# Load cookie
with open("google_cookies.json", "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    if "expiry" in cookie:
        cookie["expiry"] = int(cookie["expiry"])
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print("⚠️ Cookie bị từ chối:", cookie["name"], str(e))

# Tải lại để áp dụng cookie
driver.get("https://www.google.com")
driver.save_screenshot("google.png")

# url = "https://notebooklm.google.com/"
url = "https://chatgpt.com/"
driver.get(url)
time.sleep(2)


with open("cookie.json", "r") as f:
    cookies = json.load(f)

print("Trang hiện tại:", driver.current_url)

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
