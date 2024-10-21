
const dataHolder = document.getElementById('data-holder');
const mastery = parseFloat(dataHolder.getAttribute('data-mastery'));
const approaching = parseFloat(dataHolder.getAttribute('data-approaching'));
const needsHelp = parseFloat(dataHolder.getAttribute('data-needshelp'));
const failing = parseFloat(dataHolder.getAttribute('data-failing'));
const totalMathConfidence = parseFloat(dataHolder.getAttribute('data-total-math'));
const totalReadingConfidence = parseFloat(dataHolder.getAttribute('data-total-reading'));
const totalWritingConfidence = parseFloat(dataHolder.getAttribute('data-total-writing'));
const totalCriticalThinkingConfidence = parseFloat(dataHolder.getAttribute('data-total-critical-thinking'));
const pieData = [{
    values: [mastery, approaching, needsHelp, failing],
    labels: ['Mastery', 'Approaching', 'Needs Help', 'Failing'],
    type: 'pie'
}];
const pieLayout = { height: 400, width: 380 };
Plotly.newPlot('pie-chart', pieData, pieLayout);
const barData = [{
    x: ['Math Confidence', 'Reading Confidence', 'Writing Confidence', 'Critical Thinking Confidence'],
    y: [totalMathConfidence, totalReadingConfidence, totalWritingConfidence, totalCriticalThinkingConfidence],
    type: 'bar'
}];
const barLayout = {
    height: 400,
    width: 380,
    title: 'Class Performance Survey Results',
    xaxis: { title: 'Confidence Areas' },
    yaxis: { title: 'Confidence Level (Sum)' }
};
Plotly.newPlot('bar-chart', barData, barLayout);
const lineData = [{
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    y: [60, 65, 70, 75, 80],
    type: 'scatter'
}];
const lineLayout = {
    height: 400,
    width: 380,
    title: 'Class Mastery Over Time'
};
Plotly.newPlot('line-chart', lineData, lineLayout);
const objectives = {
    "Math Confidence": totalMathConfidence,
    "Reading Confidence": totalReadingConfidence,
    "Writing Confidence": totalWritingConfidence,
    "Critical Thinking Confidence": totalCriticalThinkingConfidence
};
let lowestObjective = '';
let lowestValue = Infinity;
for (const [objective, value] of Object.entries(objectives)) {
    if (value < lowestValue) {
        lowestValue = value;
        lowestObjective = objective;
    }
}
    const lowestObjectiveElement = document.getElementById('lowest-performing-objective');
lowestObjectiveElement.innerHTML = `<strong>Lowest-Performing Learning Objective:</strong> ${lowestObjective} (${lowestValue})`;