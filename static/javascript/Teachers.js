// Teachers.js

document.addEventListener('DOMContentLoaded', () => {
    const messages = [
        "Welcome! Ready to explore new tools and resources?",
        "Hi there! Check out the latest features to support your teaching.",
        "Hello! Find the resources you need to enhance your classroom experience.",
        "Greetings! Dive into tools designed to make your teaching easier.",
        "Welcome back! Discover new ways to engage with your students."
    ];

    function getRandomMessage() {
        const randomIndex = Math.floor(Math.random() * messages.length);
        return messages[randomIndex];
    }

    const welcomeMessageElement = document.getElementById('welcome-message');
    if (welcomeMessageElement) {
        welcomeMessageElement.textContent = getRandomMessage();
    }
});
