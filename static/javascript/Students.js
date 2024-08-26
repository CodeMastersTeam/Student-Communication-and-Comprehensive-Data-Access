// Students.js

document.addEventListener('DOMContentLoaded', () => {
    const messages = [
        "Welcome! Explore the tools and resources available for your studies.",
        "Hi there! Check out the new features to help you succeed.",
        "Hello! Find everything you need to make the most of your learning experience.",
        "Greetings! Dive into resources tailored to help you achieve your goals.",
        "Welcome back! Discover new ways to support your studies."
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
