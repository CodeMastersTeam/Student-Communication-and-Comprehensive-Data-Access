document.querySelector('.message-btn').addEventListener('mouseover', function() {
    this.style.backgroundColor = '#2980b9';
    this.style.color = '#fff';
});
document.querySelector('.message-btn').addEventListener('mouseout', function() {
    this.style.backgroundColor = '#3498db';
    this.style.color = '#000';
});

window.onload = function() {
    document.querySelector('.profile').style.opacity = '0';
    setTimeout(() => {
        document.querySelector('.profile').style.transition = 'opacity 2s ease-in';
        document.querySelector('.profile').style.opacity = '1';
    }, 500);
};

