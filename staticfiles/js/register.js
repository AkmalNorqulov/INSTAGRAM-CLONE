document.addEventListener('DOMContentLoaded', () => {
    // Show/Hide ikonkasi va Parol maydonini tanlab olish
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('passwordInput');

    // Ikonka bosilganda ishga tushadigan funksiya
    togglePassword.addEventListener('click', function (e) {
        // Parol maydonining hozirgi turini (type) aniqlash
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        
        // Yangi turini o'rnatish
        passwordInput.setAttribute('type', type);
        
        // Ikonkani almashtirish
        // .children[0] bu span ichidagi <i> elementini anglatadi
        const icon = this.children[0]; 
        
        if (type === 'text') {
            // Agar parol ko'rinadigan (text) bo'lsa, yashirish (Hide) ikonkasi (yopiq ko'z)
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            // Agar parol yashirilgan (password) bo'lsa, ko'rsatish (Show) ikonkasi (ochiq ko'z)
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });

    // *Izoh: Forma yuborilganda sahifani qayta yuklashni oldini olish uchun (ixtiyoriy)
    const signupForm = document.getElementById('signupForm');
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        console.log("Forma yuborildi (faqat namuna)");
    });
});