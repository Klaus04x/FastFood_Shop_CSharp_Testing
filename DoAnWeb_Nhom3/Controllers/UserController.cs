// DoAnWeb_Nhom3/Controllers/UserController.cs
using DoAnWeb_Nhom3.Models;
using DoAnWeb_Nhom3.Repositories;
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
        private readonly IUserRepository _userRepository;

        public UserController() : this(new UserRepository())
        {
        }

        public UserController(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

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
                    nguoidung.MANGUOIDUNG = _userRepository.GetMaxUserId() + 1;

                    // Mặc định quyền khách hàng (IDQUYEN = 1)
                    nguoidung.IDQUYEN = 1;

                    // Kiểm tra email trùng
                    if (_userRepository.EmailExists(nguoidung.EMAIL))
                    {
                        ModelState.AddModelError("EMAIL", "Email đã được sử dụng. Vui lòng chọn email khác.");
                        return View(nguoidung);
                    }

                    // Thêm người dùng mới
                    _userRepository.Add(nguoidung);
                    if (!_userRepository.SaveChanges())
                    {
                        throw new Exception("Lỗi khi lưu vào database.");
                    }

                    // Chuyển hướng đến trang đăng nhập
                    return RedirectToAction("Dangnhap");
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
                    return View(model);
                }
            }

            // Kiểm tra độ dài mật khẩu thủ công
            if (!string.IsNullOrEmpty(model.MATKHAU) && model.MATKHAU.Length < 8)
            {
                ModelState.AddModelError("MATKHAU", "Mật khẩu phải có ít nhất 8 ký tự");
                return View(model);
            }

            if (ModelState.IsValid)
            {
                // Trim dữ liệu đầu vào
                model.EMAIL = model.EMAIL?.Trim();
                model.MATKHAU = model.MATKHAU?.Trim();

                var islogin = _userRepository.GetByEmailAndPassword(model.EMAIL, model.MATKHAU);

                if (islogin != null && islogin.IDQUYEN == 2)
                {
                    Session["Admin"] = islogin;
                    return RedirectToAction("Index", "SANPHAMs", new { area = "Admin" });
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
    }
}