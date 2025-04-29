// DoAnWeb_Nhom3.Tests/Models/LoginModelTests.cs
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.ComponentModel.DataAnnotations;
using DoAnWeb_Nhom3.Models;
using System.Collections.Generic;
using System.Linq;

namespace DoAnWeb_Nhom3.Tests.Models
{
    [TestClass]
    public class LoginModelTests
    {
        [TestMethod]
        public void LoginModel_ValidatesSuccessfully_WhenAllFieldsProvided()
        {
            // Arrange
            var model = new LoginModel
            {
                EMAIL = "test@example.com",
                MATKHAU = "password123"
            };
            var context = new ValidationContext(model);
            var results = new List<ValidationResult>();

            // Act
            var isValid = Validator.TryValidateObject(model, context, results, true);

            // Assert
            Assert.IsTrue(isValid);
            Assert.AreEqual(0, results.Count);
        }

        [TestMethod]
        public void LoginModel_FailsValidation_WhenEmailIsEmpty()
        {
            // Arrange
            var model = new LoginModel
            {
                EMAIL = "",
                MATKHAU = "password123"
            };
            var context = new ValidationContext(model);
            var results = new List<ValidationResult>();

            // Act
            var isValid = Validator.TryValidateObject(model, context, results, true);

            // Assert
            Assert.IsFalse(isValid);
            Assert.IsTrue(results.Any(r => r.ErrorMessage == "Chưa nhập email"));
        }

        [TestMethod]
        public void LoginModel_FailsValidation_WhenEmailIsNull()
        {
            // Arrange
            var model = new LoginModel
            {
                EMAIL = null,
                MATKHAU = "password123"
            };
            var context = new ValidationContext(model);
            var results = new List<ValidationResult>();

            // Act
            var isValid = Validator.TryValidateObject(model, context, results, true);

            // Assert
            Assert.IsFalse(isValid);
            Assert.IsTrue(results.Any(r => r.ErrorMessage == "Chưa nhập email"));
        }

        [TestMethod]
        public void LoginModel_FailsValidation_WhenPasswordIsEmpty()
        {
            // Arrange
            var model = new LoginModel
            {
                EMAIL = "test@example.com",
                MATKHAU = ""
            };
            var context = new ValidationContext(model);
            var results = new List<ValidationResult>();

            // Act
            var isValid = Validator.TryValidateObject(model, context, results, true);

            // Assert
            Assert.IsFalse(isValid);
            Assert.IsTrue(results.Any(r => r.ErrorMessage == "Chưa nhập mật khẩu"));
        }

        [TestMethod]
        public void LoginModel_FailsValidation_WhenPasswordIsNull()
        {
            // Arrange
            var model = new LoginModel
            {
                EMAIL = "test@example.com",
                MATKHAU = null
            };
            var context = new ValidationContext(model);
            var results = new List<ValidationResult>();

            // Act
            var isValid = Validator.TryValidateObject(model, context, results, true);

            // Assert
            Assert.IsFalse(isValid);
            Assert.IsTrue(results.Any(r => r.ErrorMessage == "Chưa nhập mật khẩu"));
        }
    }
}