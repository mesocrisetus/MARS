document.getElementById('switchToRegister').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
});

document.getElementById('switchToLogin').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
});
