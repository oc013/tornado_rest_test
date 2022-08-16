/**
 * Add eventlistener that overrides default form submission to submit via AJAX
 */
let formListener = async () => {
    let formWidgetAdd = document.getElementById('form_widget_add');

    formWidgetAdd.addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = new FormData(e.target);

        await fetch('/api/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(data))
        })
        .then((response) => response.json())
        .then((data) => populateTable(true));
    });
};

/**
 * Populate the widgets table with data and optionally clear it out before hand
 * @param {Boolean} clear Set to `true` to clear table before populating
 */
let populateTable = async (clear=false) => {
    const table = document.getElementById('widget_table');
    const tbody = table.querySelector('tbody');
    const rowTemplate = document.getElementById('sample_row');

    if (clear) {
        let rows = tbody.querySelectorAll('tr');
        for (let row of rows) {
            row.remove();
        }
    }

    await fetch('/api/read', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        for (let row of data) {
            let rowClone = rowTemplate.content.cloneNode(true);
            let newRow = rowClone.querySelector('tr');

            for (let key in row) {
                rowClone.querySelector('td.' + key).innerHTML = row[key];
            }

            tbody.append(newRow);
        }
    });
};

window.onload = () => {
    formListener();
    populateTable();
};
