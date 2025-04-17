using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace DoAnWeb_Nhom3.Models
{
    [MetadataType(typeof(NGUOIDUNGMetadata))]
    public partial class NGUOIDUNG
    {
    }

    public class NGUOIDUNGMetadata
    {
        [DisplayName("Mã người dùng")]
        public int MANGUOIDUNG { get; set; }

        [Required(ErrorMessage = "Chưa nhập họ tên")]
        [StringLength(50, ErrorMessage = "Họ tên không được vượt quá 50 ký tự")]
        [RegularExpression(@"^[a-zA-ZÀ-ỹ\s]+$", ErrorMessage = "Họ tên không được chứa ký tự đặc biệt")]
        public string HOTEN { get; set; }

        [DisplayName("Email")]
        [Required(ErrorMessage = "Chưa nhập email")]
        [StringLength(100, ErrorMessage = "Email không được vượt quá 100 ký tự")]
        [EmailAddress(ErrorMessage = "Trường Email không phải là địa chỉ email hợp lệ")]
        public string EMAIL { get; set; }

        [DisplayName("Số điện thoại")]
        [Required(ErrorMessage = "Chưa nhập điện thoại")]
        [StringLength(100, ErrorMessage = "Số điện thoại không được vượt quá 100 ký tự")]
        [RegularExpression(@"^(090|091|093|094|097|098|099)\d{7}$",
            ErrorMessage = "Số điện thoại không hợp lệ")]
        public string DIENTHOAI { get; set; }

        [DisplayName("Mật khẩu")]
        [Required(ErrorMessage = "Chưa nhập mật khẩu")]
        [StringLength(50, ErrorMessage = "Mật khẩu không được vượt quá 50 ký tự")]
        [MinLength(8, ErrorMessage = "Mật khẩu phải có ít nhất 8 ký tự")]
        public string MATKHAU { get; set; }

        [DisplayName("ID Phân Quyền")]
        public int? IDQUYEN { get; set; }

        [DisplayName("Địa chỉ")]
        [Required(ErrorMessage = "Chưa nhập địa chỉ")]
        [StringLength(100, ErrorMessage = "Địa chỉ không được vượt quá 100 ký tự")]
        public string DIACHI { get; set; }
    }
}