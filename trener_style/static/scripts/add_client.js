function generatePassword(length = 12) {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let password = "";
    for (let i = 0, n = charset.length; i < length; ++i) {
        password += charset.charAt(Math.floor(Math.random() * n));
    }
    return password;
}

document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.getElementById('id_password');
    const generateButton = document.querySelector('.generate-password-btn');

    generateButton.addEventListener('click', function(e) {
        e.preventDefault();
        const newPassword = generatePassword();
        passwordInput.value = newPassword;
        passwordInput.type = 'text';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const statusSelector = document.getElementById('status');
    const activeUntilField = document.getElementById('active_until');

    function toggleActiveUntilVisibility() {
        if (statusSelector.value === 'active_until') {
            activeUntilField.parentNode.style.display = '';
        } else {
            activeUntilField.parentNode.style.display = 'none';
        }
    }
    toggleActiveUntilVisibility();
    statusSelector.addEventListener('change', toggleActiveUntilVisibility);
});