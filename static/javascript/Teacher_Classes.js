document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.student-actions .button');

    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.transform = 'scale(1.05)';
        });

        button.addEventListener('mouseout', () => {
            button.style.transform = 'scale(1)';
        });
    });

    const studentRows = document.querySelectorAll('.student-table tr');

    studentRows.forEach(row => {
        row.addEventListener('click', () => {
            row.classList.toggle('highlight');
        });
    });
});
