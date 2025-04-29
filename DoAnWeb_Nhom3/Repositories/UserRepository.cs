// DoAnWeb_Nhom3/Repositories/UserRepository.cs
using DoAnWeb_Nhom3.Models;
using System.Linq;

namespace DoAnWeb_Nhom3.Repositories
{
    public class UserRepository : IUserRepository
    {
        private readonly DoAnWeb_Nhom_3Entities1 _db;

        public UserRepository()
        {
            _db = new DoAnWeb_Nhom_3Entities1();
        }

        public UserRepository(DoAnWeb_Nhom_3Entities1 db)
        {
            _db = db;
        }

        public NGUOIDUNG GetByEmailAndPassword(string email, string password)
        {
            return _db.NGUOIDUNGs.SingleOrDefault(x => x.EMAIL.Equals(email) && x.MATKHAU.Equals(password));
        }

        public int GetMaxUserId()
        {
            return _db.NGUOIDUNGs.Max(n => (int?)n.MANGUOIDUNG) ?? 0;
        }

        public bool EmailExists(string email)
        {
            return _db.NGUOIDUNGs.Any(x => x.EMAIL.Equals(email));
        }

        public void Add(NGUOIDUNG user)
        {
            _db.NGUOIDUNGs.Add(user);
        }

        public bool SaveChanges()
        {
            try
            {
                _db.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}