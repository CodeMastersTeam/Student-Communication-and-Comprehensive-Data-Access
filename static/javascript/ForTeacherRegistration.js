document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const flashMessages = document.getElementById('flashMessages');

    // Check for saved theme preference
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        themeIcon.textContent = '🌞'; // Sun icon for light mode
    } else {
        document.body.classList.remove('dark-mode');
        themeIcon.textContent = '🌙'; // Moon icon for dark mode
    }

    themeToggle.addEventListener('click', () => {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
            themeIcon.textContent = '🌙'; // Moon icon for dark mode
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.add('dark-mode');
            themeIcon.textContent = '🌞'; // Sun icon for light mode
            localStorage.setItem('theme', 'dark');
        }
    });

    // Function to show flash messages
    function showFlashMessage(message, type = 'success') {
        flashMessages.innerHTML = `<p class="${type}">${message}</p>`;
        flashMessages.style.display = 'block';

        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000); // Hide the message after 3 seconds
    }

    // Show any flash messages on page load (if they exist)
    if (flashMessages && flashMessages.innerHTML.trim() !== '') {
        flashMessages.style.display = 'block';
        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000);
    } else {
        flashMessages.style.display = 'none';
    }
});
