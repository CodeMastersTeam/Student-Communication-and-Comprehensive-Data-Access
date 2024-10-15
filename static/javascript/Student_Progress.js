var config = { displayModeBar: false, displaylogo: false };

var pieData1 = [{
    values: [15, 25, 35, 25],
    labels: ['Math', 'Science', 'English', 'History'],
    type: 'pie'
}];
Plotly.newPlot('firstPieChart', pieData1, {}, config);

var barData1 = [{
    x: ['Math', 'Science', 'English', 'History'],
    y: [80, 90, 70, 85],
    type: 'bar'
}];
Plotly.newPlot('firstBarChart', barData1, {}, config);

var lineData1 = [{
    x: ['Q1', 'Q2', 'Q3', 'Q4'],
    y: [70, 85, 90, 95],
    mode: 'lines+markers',
    type: 'scatter'
}];
Plotly.newPlot('firstLineChart', lineData1, {}, config);

// Second Semester Charts
var pieData2 = [{
    values: [20, 30, 25, 25],
    labels: ['Math', 'Science', 'English', 'History'],
    type: 'pie'
}];
Plotly.newPlot('secondPieChart', pieData2, {}, config);

var barData2 = [{
    x: ['Math', 'Science', 'English', 'History'],
    y: [85, 88, 78, 82],
    type: 'bar'
}];
Plotly.newPlot('secondBarChart', barData2, {}, config);

var lineData2 = [{
    x: ['Q1', 'Q2', 'Q3', 'Q4'],
    y: [75, 87, 93, 97],
    mode: 'lines+markers',
    type: 'scatter'
}];
Plotly.newPlot('secondLineChart', lineData2, {}, config);
