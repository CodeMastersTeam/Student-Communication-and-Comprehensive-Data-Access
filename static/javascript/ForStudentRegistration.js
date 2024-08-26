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
        flashMessages.textContent = message;
        flashMessages.className = `flash-messages ${type} visible`; // Ensure correct class names
        flashMessages.style.display = 'block'; // Ensure display is set to block

        setTimeout(() => {
            flashMessages.classList.remove('visible');
            flashMessages.style.display = 'none'; // Hide again after timeout
        }, 3000); // Auto-hide after 3 seconds
    }

    // Clear any existing flash messages on page load
    flashMessages.style.display = 'none';
});
