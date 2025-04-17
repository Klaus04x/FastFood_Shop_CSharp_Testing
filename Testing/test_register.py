import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestRegister(unittest.TestCase):
    def setUp(self):
        chrome_driver_path = r"C:\chromedriver\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        self.driver.get("https://localhost:44335/User/Dangky")
        self.driver.maximize_window()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Đăng ký']"))
        )
        # Tắt validation phía client ngay khi load trang
        self.driver.execute_script("$(document).ready(function() { $('form').validate().cancelSubmit = true; });")
        self.driver.execute_script("document.querySelector('form').setAttribute('novalidate', 'novalidate');")

    def tearDown(self):
        self.driver.quit()

    def test_register_success(self):
        full_name = "Nguyen Van A"
        unique_email = f"newuser_{int(time.time())}@gmail.com"
        phone = "0909123456"
        password = "12345678"
        address = "123 Đường ABC"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration:", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration:", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_success_with_long_name(self):
        full_name = "Nguyen Thi Thanh Thao Van Anh"
        unique_email = f"longnameuser_{int(time.time())}@gmail.com"
        phone = "0912345678"
        password = "password12345"
        address = "456 Đường XYZ"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration (long name):", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration (long name):", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_success_with_different_phone(self):
        full_name = "Le Van B"
        unique_email = f"diffphoneuser_{int(time.time())}@gmail.com"
        phone = "0987654321"
        password = "securepass123"
        address = "789 Đường DEF"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration (different phone):", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration (different phone):", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_success_with_long_password(self):
        full_name = "Tran Van C"
        unique_email = f"longpassuser_{int(time.time())}@gmail.com"
        phone = "0935123456"
        password = "verysecurepassword123456"
        address = "101 Đường GHI"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration (long password):", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration (long password):", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_success_with_long_address(self):
        full_name = "Pham Thi D"
        unique_email = f"longaddruser_{int(time.time())}@gmail.com"
        phone = "0945123456"
        password = "password123"
        address = "Số 12, Đường Nguyễn Huệ, Phường Lê Lợi, Quận Ngô Quyền, Thành phố Hải Phòng"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration (long address):", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration (long address):", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_success_with_vietnamese_name(self):
        full_name = "Nguyễn Văn Bình"
        unique_email = f"vietnameuser_{int(time.time())}@gmail.com"
        phone = "0978123456"
        password = "password123"
        address = "123 Đường Nguyễn Trãi"

        self.driver.find_element(By.ID, "HOTEN").send_keys(full_name)
        self.driver.find_element(By.ID, "EMAIL").send_keys(unique_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys(phone)
        self.driver.find_element(By.ID, "MATKHAU").send_keys(password)
        self.driver.find_element(By.ID, "DIACHI").send_keys(address)
        
        print("URL before registration (Vietnamese name):", self.driver.current_url)
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/User/Dangnhap")
            )
            print("URL after registration (Vietnamese name):", self.driver.current_url)
        except Exception as e:
            print("Error occurred:", str(e))
            print("Current URL after error:", self.driver.current_url)
            self.fail("Đăng ký thất bại hoặc không chuyển hướng đến trang đăng nhập!")

    def test_register_invalid_name_special_characters(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen@Van#A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "HOTEN-error"))
            )
            print("Thông báo lỗi (tên không hợp lệ):", error_message.text)
            self.assertIn("Họ tên không được chứa ký tự đặc biệt", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_invalid_email(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys("invalid-email")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "EMAIL-error"))
            )
            print("Thông báo lỗi (email không hợp lệ):", error_message.text)
            self.assertIn("Trường Email không phải là địa chỉ email hợp lệ", error_message.text, "Thông báo lỗi email không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_duplicate_email(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "EMAIL-error"))
            )
            print("Thông báo lỗi (email trùng):", error_message.text)
            self.assertIn("", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_phone_less_than_10_digits(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "DIENTHOAI-error"))
            )
            print("Thông báo lỗi (số điện thoại ít hơn 10 số):", error_message.text)
            self.assertIn("Số điện thoại không hợp lệ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_phone_more_than_10_digits(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("090912345678")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "DIENTHOAI-error"))
            )
            print("Thông báo lỗi (số điện thoại nhiều hơn 10 số):", error_message.text)
            self.assertIn("Số điện thoại không hợp lệ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_phone_with_special_characters(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123#45")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "DIENTHOAI-error"))
            )
            print("Thông báo lỗi (số điện thoại chứa ký tự đặc biệt):", error_message.text)
            self.assertIn("Số điện thoại không hợp lệ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_password_too_short(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "MATKHAU-error"))
            )
            print("Thông báo lỗi (mật khẩu quá ngắn):", error_message.text)
            self.assertIn("Mật khẩu phải có ít nhất 8 ký tự", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_missing_fields(self):
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "HOTEN-error"))
            )
            print("Thông báo lỗi (thiếu họ tên):", error_message.text)
            self.assertIn("Chưa nhập họ tên", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_missing_address(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "DIACHI-error"))
            )
            print("Thông báo lỗi (thiếu địa chỉ):", error_message.text)
            self.assertIn("Chưa nhập địa chỉ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_email_too_long(self):
        long_email = "a" * 200 + "@gmail.com"
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(long_email)
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("0909123456")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "EMAIL-error"))
            )
            print("Thông báo lỗi (email quá dài):", error_message.text)
            self.assertIn("Trường Email không phải là địa chỉ email hợp lệ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

    def test_register_phone_invalid_start(self):
        self.driver.find_element(By.ID, "HOTEN").send_keys("Nguyen Van A")
        self.driver.find_element(By.ID, "EMAIL").send_keys(f"newuser_{int(time.time())}@gmail.com")
        self.driver.find_element(By.ID, "DIENTHOAI").send_keys("1234567890")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.ID, "DIACHI").send_keys("123 Đường ABC")
        
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng ký']").click()

        try:
            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "DIENTHOAI-error"))
            )
            print("Thông báo lỗi (số điện thoại bắt đầu không hợp lệ):", error_message.text)
            self.assertIn("Số điện thoại không hợp lệ", error_message.text, "Thông báo lỗi không đúng!")
        except Exception as e:
            print("Lỗi:", str(e))
            raise

if __name__ == "__main__":
    unittest.main()