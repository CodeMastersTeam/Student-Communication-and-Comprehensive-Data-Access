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

document.addEventListener('DOMContentLoaded', function() {
    const gradeInputs = document.querySelectorAll('.grade-input');

    gradeInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateGrade(this);
        });

        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                updateGrade(this);
            }
        });
    });

    function updateGrade(input) {
        const formData = new FormData();
        formData.append('subject_id', input.dataset.subjectId);
        formData.append('grade_type', input.dataset.gradeType);
        formData.append('grade_value', input.value);
        formData.append('student_id', input.dataset.studentId);
        formData.append('semester_id', input.dataset.semesterId);
        formData.append('year_id', input.dataset.yearId);

        console.log('Sending update request:', Object.fromEntries(formData));

        fetch('/update_grade', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            if (data.success) {
                console.log('Grade updated successfully');
                input.style.backgroundColor = '#90EE90';
                setTimeout(() => input.style.backgroundColor = '', 1000);
                createCharts(); // Recreate charts after updating grade
            } else {
                console.error('Failed to update grade:', data.message);
                input.style.backgroundColor = '#FFB6C1';
                setTimeout(() => input.style.backgroundColor = '', 1000);
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            input.style.backgroundColor = '#FFB6C1';
            setTimeout(() => input.style.backgroundColor = '', 1000);
            alert('An error occurred while updating the grade. Please try again.');
        });
    }

    function createCharts() {
        const subjects = [];
        const averages = [];
        const progressionData = {};
        const fullSubjectNames = {};

        document.querySelectorAll('.grade-table tbody tr').forEach(row => {
            const subjectCode = row.cells[0].textContent;
            const subjectName = row.cells[1].textContent;
            const grades = Array.from(row.querySelectorAll('input[type="number"]')).map(input => parseFloat(input.value) || 0);
            const average = grades.reduce((a, b) => a + b, 0) / grades.length;

            subjects.push(subjectCode);
            averages.push(average);
            fullSubjectNames[subjectCode] = subjectName;
            progressionData[subjectCode] = grades;

            // Make subject code clickable
            row.cells[0].style.cursor = 'pointer';
            row.cells[0].addEventListener('click', () => toggleSubjectLine(subjectCode));
        });

        const chartConfig = {
            responsive: true,
            displayModeBar: false,
            font: {
                family: 'Arial, sans-serif'
            }
        };

        // Bar Chart (Subject Performance)
        const barTrace = {
            x: subjects,
            y: averages,
            type: 'bar',
            marker: {
                color: '#3498db'
            }
        };
        const barLayout = {
            height: 400,
            width: 500,
            margin: { t: 30, b: 80, l: 50, r: 20 },
            yaxis: {range: [0, 100], title: 'Average Grade'},
            xaxis: {tickangle: -45},
            title: 'Subject Performance'
        };
        Plotly.newPlot('barChart', [barTrace], barLayout, chartConfig);

        // Line Chart (Grade Progression)
        const lineTraces = Object.entries(progressionData).map(([subject, grades]) => ({
            x: ['Prelim', 'Midterm', 'Finals'],
            y: grades,
            type: 'scatter',
            mode: 'lines+markers',
            name: subject,
            visible: true // Initially set all lines to visible
        }));
        const lineLayout = {
            height: 400,
            width: 500,
            margin: { t: 30, b: 50, l: 50, r: 20 },
            yaxis: {range: [0, 100], title: 'Grade'},
            xaxis: {title: 'Grading Period'},
            legend: {orientation: 'h', y: -0.2},
            title: 'Grade Progression'
        };
        Plotly.newPlot('lineChart', lineTraces, lineLayout, chartConfig);

        // Create legend for full subject names
        const legendContainer = document.getElementById('chartLegend');
        legendContainer.innerHTML = '<h3>Subject Name Legend:</h3><ul>';
        for (const [shortName, fullName] of Object.entries(fullSubjectNames)) {
            legendContainer.innerHTML += `<li><strong>${shortName}</strong>: ${fullName}</li>`;
        }
        legendContainer.innerHTML += '</ul>';

        // Function to toggle subject line visibility
        function toggleSubjectLine(subjectCode) {
            const lineChart = document.getElementById('lineChart');
            const update = {
                visible: lineTraces.map(trace => trace.name === subjectCode ? true : 'legendonly')
            };
            Plotly.restyle(lineChart, update);

            // Highlight the active subject in the table
            document.querySelectorAll('.grade-table tbody tr').forEach(row => {
                if (row.cells[0].textContent === subjectCode) {
                    row.classList.add('active-subject');
                } else {
                    row.classList.remove('active-subject');
                }
            });
        }
    }

    if (typeof Plotly !== 'undefined') {
        createCharts();
    } else {
        console.error('Plotly is not loaded. Charts cannot be created.');
    }
});
