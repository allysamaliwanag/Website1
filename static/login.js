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

var submitForgotPassword = document.getElementById('submitForgotPassword');
var forgotPasswordForm = document.getElementById('forgotPasswordForm');

submitForgotPassword.onclick = function () {
    forgotPasswordModal.style.display = 'none';
}
