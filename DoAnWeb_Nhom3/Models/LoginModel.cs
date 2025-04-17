using System.ComponentModel.DataAnnotations;

namespace DoAnWeb_Nhom3.Models
{
    public class LoginModel
    {
        [Required(ErrorMessage = "Chưa nhập email")]
        public string EMAIL { get; set; }

        [Required(ErrorMessage = "Chưa nhập mật khẩu")]
        public string MATKHAU { get; set; }
    }
}