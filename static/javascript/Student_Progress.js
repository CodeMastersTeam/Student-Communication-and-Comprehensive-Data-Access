function truncateLabels(labels) {
    return labels.map(label => label.length > 5 ? label.slice(0, 5) + "..." : label);
}

var subjectsElement = document.getElementById('subjects-data');
var subjectsData = JSON.parse(subjectsElement.getAttribute('data-subjects'));

var subjectsElement2 = document.getElementById('subjects-data2');
var subjectsData2 = JSON.parse(subjectsElement2.getAttribute('data-subjects2'));

function extractLabels(subjectsData) {
    return subjectsData.map(subjectTuple => subjectTuple[0]); 
}

var truncatedLabels1 = truncateLabels(extractLabels(subjectsData));
var truncatedLabels2 = truncateLabels(extractLabels(subjectsData2));

var config = { displayModeBar: false, displaylogo: false };

var pieData1 = [{
    values: [15, 25, 35, 25],
    labels: truncatedLabels1, 
    type: 'pie'
}];
Plotly.newPlot('firstPieChart', pieData1, {}, config);

var barData1 = [{
    x: truncatedLabels1,
    y: [80, 90, 70, 85],
    type: 'bar'
}];
Plotly.newPlot('firstBarChart', barData1, {}, config);

var lineData1 = [{
    x: truncatedLabels1,  
    y: [70, 85, 90, 95],
    mode: 'lines+markers',
    type: 'scatter'
}];
Plotly.newPlot('firstLineChart', lineData1, {}, config);

var pieData2 = [{
    values: [20, 30, 25, 25],
    labels: truncatedLabels2, 
    type: 'pie'
}];
Plotly.newPlot('secondPieChart', pieData2, {}, config);

var barData2 = [{
    x: truncatedLabels2, 
    y: [85, 88, 78, 82],
    type: 'bar'
}];
Plotly.newPlot('secondBarChart', barData2, {}, config);

var lineData2 = [{
    x: truncatedLabels2,  
    y: [75, 87, 93, 97],
    mode: 'lines+markers',
    type: 'scatter'
}];
Plotly.newPlot('secondLineChart', lineData2, {}, config);

function renderFullSubjectNames(subjects, elementId) {
    var subjectList = document.getElementById(elementId);
    subjects.forEach(subject => {
        var listItem = document.createElement('li');
        listItem.textContent = subject;
        subjectList.appendChild(listItem);
    });
}

var fullSubjects1 = extractLabels(subjectsData);
renderFullSubjectNames(fullSubjects1, 'subject-list');

var fullSubjects2 = extractLabels(subjectsData2);
renderFullSubjectNames(fullSubjects2, 'subject-list2');
