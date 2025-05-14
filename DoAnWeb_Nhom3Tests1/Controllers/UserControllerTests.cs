using Microsoft.VisualStudio.TestTools.UnitTesting;
using DoAnWeb_Nhom3.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DoAnWeb_Nhom3.Models;
using System.Web.Mvc;

namespace DoAnWeb_Nhom3.Controllers.Tests
{
    [TestClass()]
    public class UserControllerTests
    {
        [TestClass()]
        public class UserControllerTests1
        {
            private UserController _controller;

            [TestInitialize]
            public void Setup()
            {
                _controller = new UserController();
            }

            [TestMethod]
            public void Dangnhap_Get_ReturnsView()
            {
                // Act
                var result = _controller.Dangnhap() as ViewResult;

                // Assert
                Assert.IsNotNull(result);
                Assert.IsInstanceOfType(result.Model, typeof(LoginModel));
            }

            [TestMethod]
            public void Dangnhap_Post_WithInvalidEmail_ReturnsView()
            {
                // Arrange
                var model = new LoginModel { EMAIL = "invalid-email", MATKHAU = "password123" };

                // Act
                var result = _controller.Dangnhap(model) as ViewResult;

                // Assert
                Assert.IsNotNull(result);
                Assert.IsTrue(result.ViewData.ModelState.ContainsKey("EMAIL"));
                Assert.AreEqual("Định dạng email không hợp lệ", result.ViewData.ModelState["EMAIL"].Errors[0].ErrorMessage);
            }

            [TestMethod]
            public void Dangnhap_Post_WithShortPassword_ReturnsView()
            {
                // Arrange
                var model = new LoginModel { EMAIL = "test@example.com", MATKHAU = "short" };

                // Act
                var result = _controller.Dangnhap(model) as ViewResult;

                // Assert
                Assert.IsNotNull(result);
                Assert.IsTrue(result.ViewData.ModelState.ContainsKey("MATKHAU"));
                Assert.AreEqual("Mật khẩu phải có ít nhất 8 ký tự", result.ViewData.ModelState["MATKHAU"].Errors[0].ErrorMessage);
            }
        }
    }
}