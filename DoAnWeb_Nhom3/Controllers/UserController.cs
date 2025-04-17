using DoAnWeb_Nhom3.Models;
using System;
using System.Data.Entity.Infrastructure;
using System.Data.Entity.Validation;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web.Mvc;

namespace DoAnWeb_Nhom3.Controllers
{
    public class UserController : Controller
    {
        private DoAnWeb_Nhom_3Entities1 db = new DoAnWeb_Nhom_3Entities1();

        // GET: User/Dangky
        public ActionResult Dangky()
        {
            return View();
        }

        // ĐĂNG KÝ PHƯƠNG THỨC POST
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Dangky(NGUOIDUNG nguoidung)
        {
            if (ModelState.IsValid)
            {
                try
                {
                    // Tăng mã người dùng lên
                    var maMax = db.NGUOIDUNGs.Max(n => (int?)n.MANGUOIDUNG) ?? 0;
                    nguoidung.MANGUOIDUNG = maMax + 1;

                    // Mặc định quyền khách hàng (IDQUYEN = 1)
                    nguoidung.IDQUYEN = 1;

                    // Thêm người dùng mới
                    db.NGUOIDUNGs.Add(nguoidung);
                    db.SaveChanges();

                    // Chuyển hướng đến trang đăng nhập
                    return RedirectToAction("Dangnhap");
                }
                catch (DbUpdateException ex) when (ex.InnerException?.Message.Contains("UNIQUE") == true)
                {
                    ModelState.AddModelError("EMAIL", "Email đã được sử dụng. Vui lòng chọn email khác.");
                }
                catch (DbEntityValidationException ex)
                {
                    var errorMessages = ex.EntityValidationErrors
                        .SelectMany(x => x.ValidationErrors)
                        .Select(x => $"{x.PropertyName}: {x.ErrorMessage}");
                    var fullErrorMessage = string.Join("; ", errorMessages);
                    ModelState.AddModelError("", $"Lỗi xác thực: {fullErrorMessage}");
                }
                catch (Exception ex)
                {
                    var innerException = ex.InnerException?.Message ?? "Không có inner exception";
                    var stackTrace = ex.InnerException?.StackTrace ?? ex.StackTrace;
                    ModelState.AddModelError("", $"Lỗi: {ex.Message}. Inner Exception: {innerException}. Stack Trace: {stackTrace}");
                }
            }
            else
            {
                var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage);
                ModelState.AddModelError("", $"ModelState không hợp lệ: {string.Join("; ", errors)}");
            }

            return View(nguoidung);
        }

        // GET: User/Dangnhap
        public ActionResult Dangnhap()
        {
            return View(new LoginModel());
        }

        // ĐĂNG NHẬP PHƯƠNG THỨC POST
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Dangnhap(LoginModel model)
        {
            // Kiểm tra định dạng email thủ công
            if (!string.IsNullOrEmpty(model.EMAIL))
            {
                string emailPattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$";
                if (!Regex.IsMatch(model.EMAIL, emailPattern))
                {
                    ModelState.AddModelError("EMAIL", "Định dạng email không hợp lệ");
                    return View(model); // Trả về view ngay nếu email không hợp lệ
                }
            }

            // Kiểm tra độ dài mật khẩu thủ công
            if (!string.IsNullOrEmpty(model.MATKHAU) && model.MATKHAU.Length < 8)
            {
                ModelState.AddModelError("MATKHAU", "Mật khẩu phải có ít nhất 8 ký tự");
                return View(model); // Trả về view ngay nếu mật khẩu không hợp lệ
            }

            if (ModelState.IsValid)
            {
                // Trim dữ liệu đầu vào
                model.EMAIL = model.EMAIL?.Trim();
                model.MATKHAU = model.MATKHAU?.Trim();

                var islogin = db.NGUOIDUNGs.SingleOrDefault(x => x.EMAIL.Equals(model.EMAIL) && x.MATKHAU.Equals(model.MATKHAU));

                if (islogin != null && islogin.IDQUYEN == 2)
                {
                    Session["Admin"] = islogin;
                    return RedirectToAction("Index", "Admin/SANPHAMs");
                }
                else if (islogin != null && islogin.IDQUYEN == 1)
                {
                    Session["use"] = islogin;
                    return RedirectToAction("Index", "Home");
                }
                else
                {
                    ModelState.AddModelError("", "Đăng nhập thất bại. Email hoặc mật khẩu không đúng.");
                }
            }

            return View(model);
        }

        // ĐĂNG XUẤT
        public ActionResult DangXuat()
        {
            Session["use"] = null;
            Session["GioHang"] = null;
            return RedirectToAction("Index", "Home");
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}