// DoAnWeb_Nhom3/Repositories/IUserRepository.cs
using DoAnWeb_Nhom3.Models;

namespace DoAnWeb_Nhom3.Repositories
{
    public interface IUserRepository
    {
        NGUOIDUNG GetByEmailAndPassword(string email, string password);
        int GetMaxUserId();
        bool EmailExists(string email);
        void Add(NGUOIDUNG user);
        bool SaveChanges();
    }
}