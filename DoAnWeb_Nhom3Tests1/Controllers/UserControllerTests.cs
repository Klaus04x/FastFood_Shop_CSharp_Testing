using Microsoft.VisualStudio.TestTools.UnitTesting;
using DoAnWeb_Nhom3.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DoAnWeb_Nhom3.Controllers.Tests
{
    [TestClass()]
    public class UserControllerTests
    {
        [TestMethod()]
        public void DangnhapTest()
        {
            DoAnWeb_Nhom3.Controllers.UserController userController = new DoAnWeb_Nhom3.Controllers.UserController();
            userController.Dangnhap();
            Assert.IsNotNull(userController);
        }
    }
}