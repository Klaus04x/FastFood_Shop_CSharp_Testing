// DoAnWeb_Nhom3.Tests/Controllers/UserControllerTests.cs
using FluentAssertions;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System;
using System.Collections.Generic;
using System.Data.Entity.Infrastructure;
using System.Data.Entity.Validation;
using System.Web;
using System.Web.Mvc;
using DoAnWeb_Nhom3.Controllers;
using DoAnWeb_Nhom3.Models;
using DoAnWeb_Nhom3.Repositories;

namespace DoAnWeb_Nhom3.Tests.Controllers
{
    [TestClass]
    public class UserControllerTests
    {
        private Mock<IUserRepository> _userRepositoryMock;
        private UserController _controller;
        private Mock<HttpSessionStateBase> _sessionMock;
        private Mock<HttpContextBase> _httpContextMock;

        [TestInitialize]
        public void Setup()
        {
            _userRepositoryMock = new Mock<IUserRepository>();
            _sessionMock = new Mock<HttpSessionStateBase>();
            _httpContextMock = new Mock<HttpContextBase>();
            _httpContextMock.Setup(c => c.Session).Returns(_sessionMock.Object);

            _controller = new UserController(_userRepositoryMock.Object)
            {
                ControllerContext = new ControllerContext
                {
                    HttpContext = _httpContextMock.Object
                }
            };
        }

        #region Dangnhap Tests

        [TestMethod]
        public void Dangnhap_Get_ReturnsViewWithLoginModel()
        {
            // Act
            var result = _controller.Dangnhap() as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsInstanceOfType(result.Model, typeof(LoginModel));
            result.Model.Should().BeOfType<LoginModel>();
        }

        [TestMethod]
        public void Dangnhap_Post_ReturnsView_WhenEmailFormatInvalid()
        {
            // Arrange
            var model = new LoginModel { EMAIL = "invalid-email", MATKHAU = "password123" };

            // Act
            var result = _controller.Dangnhap(model) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey("EMAIL"));
            result.ViewData.ModelState["EMAIL"].Errors[0].ErrorMessage.Should().Be("Định dạng email không hợp lệ");
            result.Model.Should().Be(model);
        }

        [TestMethod]
        public void Dangnhap_Post_ReturnsView_WhenPasswordTooShort()
        {
            // Arrange
            var model = new LoginModel { EMAIL = "test@example.com", MATKHAU = "short" };

            // Act
            var result = _controller.Dangnhap(model) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey("MATKHAU"));
            result.ViewData.ModelState["MATKHAU"].Errors[0].ErrorMessage.Should().Be("Mật khẩu phải có ít nhất 8 ký tự");
            result.Model.Should().Be(model);
        }

        [TestMethod]
        public void Dangnhap_Post_ReturnsView_WhenModelStateInvalid()
        {
            // Arrange
            var model = new LoginModel { EMAIL = null, MATKHAU = null };
            _controller.ModelState.AddModelError("EMAIL", "Chưa nhập email");
            _controller.ModelState.AddModelError("MATKHAU", "Chưa nhập mật khẩu");

            // Act
            var result = _controller.Dangnhap(model) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey("EMAIL"));
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey("MATKHAU"));
            result.Model.Should().Be(model);
        }

        [TestMethod]
        public void Dangnhap_Post_RedirectsToAdmin_WhenAdminCredentialsValid()
        {
            // Arrange
            var model = new LoginModel { EMAIL = "admin@example.com", MATKHAU = "password123" };
            var user = new NGUOIDUNG
            {
                MANGUOIDUNG = 1,
                EMAIL = model.EMAIL,
                MATKHAU = model.MATKHAU,
                IDQUYEN = 2
            };
            _userRepositoryMock.Setup(repo => repo.GetByEmailAndPassword(model.EMAIL.Trim(), model.MATKHAU.Trim())).Returns(user);

            // Act
            var result = _controller.Dangnhap(model) as RedirectToRouteResult;

            // Assert
            Assert.IsNotNull(result);
            result.RouteValues["action"].Should().Be("Index");
            result.RouteValues["controller"].Should().Be("SANPHAMs");
            result.RouteValues["area"].Should().Be("Admin");
            _sessionMock.Verify(s => s["Admin"] = user, Times.Once());
        }

        [TestMethod]
        public void Dangnhap_Post_RedirectsToHome_WhenCustomerCredentialsValid()
        {
            // Arrange
            var model = new LoginModel { EMAIL = "user@example.com", MATKHAU = "password123" };
            var user = new NGUOIDUNG
            {
                MANGUOIDUNG = 2,
                EMAIL = model.EMAIL,
                MATKHAU = model.MATKHAU,
                IDQUYEN = 1
            };
            _userRepositoryMock.Setup(repo => repo.GetByEmailAndPassword(model.EMAIL.Trim(), model.MATKHAU.Trim())).Returns(user);

            // Act
            var result = _controller.Dangnhap(model) as RedirectToRouteResult;

            // Assert
            Assert.IsNotNull(result);
            result.RouteValues["action"].Should().Be("Index");
            result.RouteValues["controller"].Should().Be("Home");
            _sessionMock.Verify(s => s["use"] = user, Times.Once());
        }

        [TestMethod]
        public void Dangnhap_Post_ReturnsView_WhenCredentialsInvalid()
        {
            // Arrange
            var model = new LoginModel { EMAIL = "wrong@example.com", MATKHAU = "wrongpassword" };
            _userRepositoryMock.Setup(repo => repo.GetByEmailAndPassword(model.EMAIL.Trim(), model.MATKHAU.Trim())).Returns((NGUOIDUNG)null);

            // Act
            var result = _controller.Dangnhap(model) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey(""));
            result.ViewData.ModelState[""].Errors[0].ErrorMessage.Should().Be("Đăng nhập thất bại. Email hoặc mật khẩu không đúng.");
            result.Model.Should().Be(model);
        }

        #endregion

        #region Dangky Tests

        [TestMethod]
        public void Dangky_Get_ReturnsView()
        {
            // Act
            var result = _controller.Dangky() as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsNull(result.Model);
        }

        [TestMethod]
        public void Dangky_Post_RedirectsToDangnhap_WhenRegistrationSuccessful()
        {
            // Arrange
            var user = new NGUOIDUNG
            {
                HOTEN = "Test User",
                EMAIL = "test@example.com",
                DIENTHOAI = "1234567890",
                MATKHAU = "password123",
                DIACHI = "123 Street"
            };
            _userRepositoryMock.Setup(repo => repo.GetMaxUserId()).Returns(10);
            _userRepositoryMock.Setup(repo => repo.EmailExists(user.EMAIL)).Returns(false);
            _userRepositoryMock.Setup(repo => repo.SaveChanges()).Returns(true);

            // Act
            var result = _controller.Dangky(user) as RedirectToRouteResult;

            // Assert
            Assert.IsNotNull(result);
            result.RouteValues["action"].Should().Be("Dangnhap");
            _userRepositoryMock.Verify(repo => repo.Add(It.Is<NGUOIDUNG>(u => u.MANGUOIDUNG == 11 && u.IDQUYEN == 1)), Times.Once());
            _userRepositoryMock.Verify(repo => repo.SaveChanges(), Times.Once());
        }

        [TestMethod]
        public void Dangky_Post_ReturnsView_WhenEmailExists()
        {
            // Arrange
            var user = new NGUOIDUNG
            {
                HOTEN = "Test User",
                EMAIL = "existing@example.com",
                DIENTHOAI = "1234567890",
                MATKHAU = "password123",
                DIACHI = "123 Street"
            };
            _userRepositoryMock.Setup(repo => repo.EmailExists(user.EMAIL)).Returns(true);

            // Act
            var result = _controller.Dangky(user) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey("EMAIL"));
            result.ViewData.ModelState["EMAIL"].Errors[0].ErrorMessage.Should().Be("Email đã được sử dụng. Vui lòng chọn email khác.");
            result.Model.Should().Be(user);
        }

        [TestMethod]
        public void Dangky_Post_ReturnsView_WhenModelStateInvalid()
        {
            // Arrange
            var user = new NGUOIDUNG();
            _controller.ModelState.AddModelError("HOTEN", "Chưa nhập họ tên");
            _controller.ModelState.AddModelError("EMAIL", "Chưa nhập email");

            // Act
            var result = _controller.Dangky(user) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey(""));
            result.ViewData.ModelState[""].Errors[0].ErrorMessage.Should().Contain("Chưa nhập họ tên");
            result.ViewData.ModelState[""].Errors[0].ErrorMessage.Should().Contain("Chưa nhập email");
            result.Model.Should().Be(user);
        }

        [TestMethod]
        public void Dangky_Post_ReturnsView_WhenDbEntityValidationExceptionThrown()
        {
            // Arrange
            var user = new NGUOIDUNG
            {
                HOTEN = "Test User",
                EMAIL = "test@example.com",
                DIENTHOAI = "1234567890",
                MATKHAU = "password123",
                DIACHI = "123 Street"
            };
            _userRepositoryMock.Setup(repo => repo.GetMaxUserId()).Returns(10);
            _userRepositoryMock.Setup(repo => repo.EmailExists(user.EMAIL)).Returns(false);
            _userRepositoryMock.Setup(repo => repo.SaveChanges()).Throws(new DbEntityValidationException(
                "Validation failed",
                new List<DbEntityValidationResult>
                {
                    new DbEntityValidationResult(null, new List<DbValidationError>
                    {
                        new DbValidationError("HOTEN", "Họ tên không hợp lệ")
                    })
                }));

            // Act
            var result = _controller.Dangky(user) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey(""));
            result.ViewData.ModelState[""].Errors[0].ErrorMessage.Should().Contain("HOTEN: Họ tên không hợp lệ");
            result.Model.Should().Be(user);
        }

        [TestMethod]
        public void Dangky_Post_ReturnsView_WhenGenericExceptionThrown()
        {
            // Arrange
            var user = new NGUOIDUNG
            {
                HOTEN = "Test User",
                EMAIL = "test@example.com",
                DIENTHOAI = "1234567890",
                MATKHAU = "password123",
                DIACHI = "123 Street"
            };
            _userRepositoryMock.Setup(repo => repo.GetMaxUserId()).Returns(10);
            _userRepositoryMock.Setup(repo => repo.EmailExists(user.EMAIL)).Returns(false);
            _userRepositoryMock.Setup(repo => repo.SaveChanges()).Throws(new Exception("Database error"));

            // Act
            var result = _controller.Dangky(user) as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.IsTrue(result.ViewData.ModelState.ContainsKey(""));
            result.ViewData.ModelState[""].Errors[0].ErrorMessage.Should().Contain("Lỗi: Database error");
            result.Model.Should().Be(user);
        }

        #endregion

        #region DangXuat Tests

        [TestMethod]
        public void DangXuat_ClearsSessionAndRedirectsToHome()
        {
            // Act
            var result = _controller.DangXuat() as RedirectToRouteResult;

            // Assert
            Assert.IsNotNull(result);
            result.RouteValues["action"].Should().Be("Index");
            result.RouteValues["controller"].Should().Be("Home");
            _sessionMock.Verify(s => s["use"] = null, Times.Once());
            _sessionMock.Verify(s => s["GioHang"] = null, Times.Once());
        }

        #endregion
    }
}