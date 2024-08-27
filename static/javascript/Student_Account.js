const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeIcon.textContent = document.body.classList.contains('dark-mode') ? '🌞' : '🌙';
});

document.getElementById('profile_picture').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
    document.getElementById('file-name').textContent = fileName;
});