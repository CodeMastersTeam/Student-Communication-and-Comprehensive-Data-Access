document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        themeIcon.textContent = '🌞';
    } else {
        document.body.classList.remove('dark-mode');
        themeIcon.textContent = '🌙'; 
    }

    themeToggle.addEventListener('click', () => {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
            themeIcon.textContent = '🌙'; 
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.add('dark-mode');
            themeIcon.textContent = '🌞'; 
            localStorage.setItem('theme', 'dark');
        }
    });
});