document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const password1 = document.querySelector('input[name="updatepassword1"]');
    const password2 = document.querySelector('input[name="updatepassword2"]');

    form.addEventListener('submit', function(event) {
        if (password1.value !== password2.value) {
            event.preventDefault(); 
            alert('Passwords do not match. Please try again.');
        }
    });
});
