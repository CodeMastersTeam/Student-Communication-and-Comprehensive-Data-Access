document.getElementById('profile_picture').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
    document.getElementById('file-name').textContent = fileName;
});

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const flashMessages = document.querySelector('.flash-messages');
        if (flashMessages) {
            flashMessages.style.transition = 'opacity 0.5s ease';  
            flashMessages.style.opacity = 0;

            setTimeout(() => {
                flashMessages.style.display = 'none';
            }, 500); 
        }
    }, 3000);  
});