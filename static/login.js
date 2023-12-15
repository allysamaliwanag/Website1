// script.js

// JavaScript code for handling the modal
var forgotPasswordModal = document.getElementById('forgotPasswordModal');
var forgotPasswordLink = document.getElementById('forgotPasswordLink');
var closeForgotPasswordModal = document.getElementById('closeForgotPasswordModal');

forgotPasswordLink.onclick = function () {
    forgotPasswordModal.style.display = 'block';
}

closeForgotPasswordModal.onclick = function () {
    forgotPasswordModal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == forgotPasswordModal) {
        forgotPasswordModal.style.display = 'none';
    }
}

// Add logic for handling the "Forgot Password" form submission here
var submitForgotPassword = document.getElementById('submitForgotPassword');
var forgotPasswordForm = document.getElementById('forgotPasswordForm');

submitForgotPassword.onclick = function () {
    // Implement logic for submitting the "Forgot Password" form
    // You may use AJAX to send the request to the server
    // Example: You can display a success message or an error message
    // based on the response from the server
    // After handling the submission, you may close the modal
    forgotPasswordModal.style.display = 'none';
}
