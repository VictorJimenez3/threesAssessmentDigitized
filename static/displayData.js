/*
Programmed by: Victor Jimenez
*/

function displayClickData(clickDataFromServer) {
    const resultTableBody = document.getElementById('result-table-body');
    if (!resultTableBody) {
        console.error("Element with ID 'result-table-body' not found in the DOM.");
        return;
    }

    resultTableBody.innerHTML = ''; // Clear existing rows

    // Log the received data
    console.log("Populating table with clickData:", clickDataFromServer);

    clickDataFromServer.forEach(entry => {
        const [row, col, index, time] = entry;

        const resultRow = document.createElement('tr');

        // Each cell in the row
        const checkedCell = document.createElement('td');
        checkedCell.textContent = "✔️";  // Example value, replace if needed
        resultRow.appendChild(checkedCell);

        const rowCell = document.createElement('td');
        rowCell.textContent = row;
        resultRow.appendChild(rowCell);

        const colCell = document.createElement('td');
        colCell.textContent = col;
        resultRow.appendChild(colCell);

        const indexCell = document.createElement('td');
        indexCell.textContent = index;
        resultRow.appendChild(indexCell);

        const charCell = document.createElement('td');
        charCell.textContent = tableData[row][col].toString()[index];
        resultRow.appendChild(charCell);

        const timeCell = document.createElement('td');
        timeCell.textContent = time;
        resultRow.appendChild(timeCell);

        resultTableBody.appendChild(resultRow);
    });
}
