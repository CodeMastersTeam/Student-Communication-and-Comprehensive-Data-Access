function searchResources() {
    const input = document.getElementById('search-bar').value.toLowerCase();
    const table = document.getElementById('resource-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let matchFound = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].innerText.toLowerCase().includes(input)) {
                matchFound = true;
                break;
            }
        }
        rows[i].style.display = matchFound ? '' : 'none';
    }
}