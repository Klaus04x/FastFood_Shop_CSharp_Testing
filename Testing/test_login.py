import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginUnit(unittest.TestCase):
    def setUp(self):
        chrome_driver_path = r"C:\chromedriver\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        self.driver.get("https://localhost:44335/User/Dangnhap")
        self.driver.maximize_window()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Đăng nhập']"))
        )

        # Tắt validation phía client triệt để
        self.driver.execute_script("""
            // Thêm thuộc tính novalidate để tắt validation HTML5
            document.querySelector('form').setAttribute('novalidate', 'novalidate');
            
            // Xóa các script validation nếu chúng đã được tải
            var scripts = document.getElementsByTagName('script');
            for (var i = scripts.length - 1; i >= 0; i--) {
                if (scripts[i].src.includes('jquery.validate') || scripts[i].src.includes('unobtrusive')) {
                    scripts[i].parentNode.removeChild(scripts[i]);
                }
            }
            
            // Tắt validation nếu jQuery Validation đã được khởi tạo
            if (typeof jQuery !== 'undefined' && jQuery().validate) {
                jQuery('form').removeData('validator').removeData('unobtrusiveValidation');
                jQuery.validator.unobtrusive = undefined;
                jQuery('form').off('submit.validate');
                jQuery('form').off('focusout.validate');
                jQuery('form').off('keyup.validate');
            }
            
            // Xóa các thuộc tính validation trên các input
            var inputs = document.querySelectorAll('input, textarea');
            inputs.forEach(function(input) {
                for (var attr in input.dataset) {
                    if (attr.startsWith('val')) {
                        delete input.dataset[attr];
                    }
                }
            });
        """)

    def tearDown(self):
        self.driver.quit()

    def test_login_success_customer(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        WebDriverWait(self.driver, 30).until(
            EC.url_to_be("https://localhost:44335/")
        )
        print("URL sau khi đăng nhập (khách):", self.driver.current_url)

        try:
            user_email = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Xin chào')]"))
            )
            print("User email text:", user_email.text)
            self.assertIn("customer@gmail.com", user_email.text, "Đăng nhập thất bại, không tìm thấy email người dùng!")
        except Exception as e:
            print("Lỗi khi tìm email người dùng:", str(e))
            print("Nguồn trang:", self.driver.page_source)
            raise

    def test_login_success_admin(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("admin@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://localhost:44335/Admin/SANPHAMs")
            )
            print("URL sau khi đăng nhập (admin):", self.driver.current_url)
            self.assertEqual(self.driver.current_url, "https://localhost:44335/Admin/SANPHAMs", "Không chuyển hướng đến trang quản lý sản phẩm!")
        except Exception as e:
            print("Lỗi chuyển hướng:", str(e))
            print("URL hiện tại:", self.driver.current_url)
            print("Nguồn trang:", self.driver.page_source)
            raise

    def test_login_invalid_credentials(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        error_message = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        print("Thông báo lỗi (sai thông tin):", error_message.text)

        self.assertIn("Đăng nhập thất bại. Email hoặc mật khẩu không đúng.", error_message.text, "Thông báo lỗi không đúng!")

    def test_login_missing_fields(self):
        self.driver.find_element(By.ID, "EMAIL").clear()
        self.driver.find_element(By.ID, "MATKHAU").clear()
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        try:
            email_error = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "EMAIL-error"))
            )
            password_error = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "MATKHAU-error"))
            )
            print("Thông báo lỗi (thiếu email):", email_error.text)
            print("Thông báo lỗi (thiếu mật khẩu):", password_error.text)

            self.assertIn("Chưa nhập email", email_error.text, "Thông báo lỗi email không đúng!")
            self.assertIn("Chưa nhập mật khẩu", password_error.text, "Thông báo lỗi mật khẩu không đúng!")
        except Exception as e:
            print("Lỗi khi tìm thông báo lỗi:", str(e))
            print("Nguồn trang:", self.driver.page_source)
            raise

    # Test case 1: Đăng nhập với email không tồn tại
    def test_login_nonexistent_email(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("nonexistent@example.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        error_message = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        print("Thông báo lỗi (email không tồn tại):", error_message.text)
        self.assertIn("Đăng nhập thất bại. Email hoặc mật khẩu không đúng.", error_message.text, "Thông báo lỗi không đúng!")

    # Test case 2: Đăng nhập với mật khẩu sai nhưng email đúng
    def test_login_wrong_password(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("wrong123")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        error_message = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        print("Thông báo lỗi (mật khẩu sai):", error_message.text)
        self.assertIn("Đăng nhập thất bại. Email hoặc mật khẩu không đúng.", error_message.text, "Thông báo lỗi không đúng!")

    # Test case 3: Đăng nhập với email có định dạng sai
    def test_login_invalid_email_format(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("invalid-email")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        email_error = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "EMAIL-error"))
        )
        print("Thông báo lỗi (email định dạng sai):", email_error.text)
        self.assertIn("Định dạng email không hợp lệ", email_error.text, "Thông báo lỗi email không đúng!")

    # Test case 4: Đăng nhập với mật khẩu ngắn (dưới giới hạn)
    def test_login_short_password(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("123")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        password_error = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "MATKHAU-error"))
        )
        print("Thông báo lỗi (mật khẩu ngắn):", password_error.text)
        self.assertIn("Mật khẩu phải có ít nhất 8 ký tự", password_error.text, "Thông báo lỗi mật khẩu không đúng!")

    # Test case 5: Đăng nhập với email có khoảng trắng ở đầu/cuối
    def test_login_invalid_email_format(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("  customer@gmail.com  ")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        email_error = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "EMAIL-error"))
        )
        print("Thông báo lỗi (email định dạng sai):", email_error.text)
        self.assertIn("Định dạng email không hợp lệ", email_error.text, "Thông báo lỗi email không đúng!")

    # Test case 6: Đăng nhập với mật khẩu có khoảng trắng ở đầu/cuối
    def test_login_password_with_whitespace(self):
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("  12345678  ")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        WebDriverWait(self.driver, 30).until(
            EC.url_to_be("https://localhost:44335/")
        )
        print("URL sau khi đăng nhập (mật khẩu có khoảng trắng):", self.driver.current_url)
        user_email = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Xin chào')]"))
        )
        print("User email text:", user_email.text)
        self.assertIn("customer@gmail.com", user_email.text, "Đăng nhập thất bại với mật khẩu có khoảng trắng!")

    # Test case 7: Đăng nhập nhiều lần thất bại liên tiếp
    def test_login_multiple_failed_attempts(self):
        for i in range(3):
            self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
            self.driver.find_element(By.ID, "MATKHAU").send_keys(f"wrongpassword{i}")
            self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

            error_message = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            print(f"Thông báo lỗi (lần thất bại {i+1}):", error_message.text)
            self.assertIn("Đăng nhập thất bại. Email hoặc mật khẩu không đúng.", error_message.text, f"Thông báo lỗi không đúng ở lần thử {i+1}!")

            # Reset form để thử lại
            self.driver.find_element(By.ID, "EMAIL").clear()
            self.driver.find_element(By.ID, "MATKHAU").clear()

    # Test case 8: Đăng nhập thành công sau khi đăng xuất
    def test_login_after_logout(self):
        # Đăng nhập lần đầu
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        WebDriverWait(self.driver, 30).until(
            EC.url_to_be("https://localhost:44335/")
        )

        # Đăng xuất
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'ĐĂNG XUẤT')]").click()
        WebDriverWait(self.driver, 30).until(
            EC.url_to_be("https://localhost:44335/")
        )

        # Truy cập lại trang đăng nhập
        self.driver.get("https://localhost:44335/User/Dangnhap")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Đăng nhập']"))
        )

        # Đăng nhập lại
        self.driver.find_element(By.ID, "EMAIL").send_keys("customer@gmail.com")
        self.driver.find_element(By.ID, "MATKHAU").send_keys("12345678")
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Đăng nhập']").click()

        WebDriverWait(self.driver, 30).until(
            EC.url_to_be("https://localhost:44335/")
        )
        print("URL sau khi đăng nhập lại (sau đăng xuất):", self.driver.current_url)
        user_email = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Xin chào')]"))
        )
        print("User email text (sau đăng xuất):", user_email.text)
        self.assertIn("customer@gmail.com", user_email.text, "Đăng nhập thất bại sau khi đăng xuất!")

if __name__ == "__main__":
    unittest.main()