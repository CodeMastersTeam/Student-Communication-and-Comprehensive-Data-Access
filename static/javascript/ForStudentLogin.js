document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const flashMessages = document.querySelector('.flash-messages');
        if (flashMessages) {
            flashMessages.style.opacity = 0;
            setTimeout(() => flashMessages.style.display = 'none', 500); 
        }
    }, 3000); 
});
