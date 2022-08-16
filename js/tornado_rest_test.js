/**
 * Add eventlistener that overrides default form submission to submit via AJAX
 * The same form also allows record create and update and is handled thusly here.
 */
let formListener = async () => {
    let formWidget = document.getElementById('form_widget');

    formWidget.addEventListener('submit', async (e) => {
        e.preventDefault();

        let mode = document.getElementById('form_mode').value;

        const data = new FormData(e.target);

        if (mode == 'create') {
            var apiUrl = '/api/create';
        } else if (mode == 'update') {
            var apiUrl = '/api/update';
        } else {
            return false;
        }

        await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(data))
        })
        .then((response) => response.json())
        .then((data) => {
            e.target.reset();
            populateTable(true);
        });
    });

    /**
     * Reset form also sets it back to add mode
     */
    formWidget.addEventListener('reset', (e) => {
        document.getElementById('form_mode').value = 'create';
        document.getElementById('widget_id').value = '';
        document.querySelector('form#form_widget fieldset legend').innerHTML = 'Add Widget';
        document.querySelector('form#form_widget fieldset button[type="submit"]').innerHTML = 'Add Widget';
    });
};

/**
 * Add listener to magnifying glass to inspect record in more detail
 */
let inspectListeners = async () => {
    const inspectButtons = document.querySelectorAll('span.inspect');

    for (let inspectButton of inspectButtons) {
        inspectButton.addEventListener('click', async (e) => {
            e.stopPropagation();

            let parentRow = e.target.closest('tr');
            let id = parentRow.dataset.id;


            await fetch('/api/read', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: id})
            })
            .then((response) => response.json())
            .then((data) => {
                let inspectDiv = document.querySelector('div#inspect');
                let inspectDivContent = inspectDiv.querySelector('span.content');

                let outputInspect = '';
                for (let element in data) {
                    outputInspect += element + ': ' + data[element] + '<br>';
                }
                inspectDivContent.innerHTML = outputInspect;

                inspectDiv.classList.add('show');
                inspectDiv.style.top = e.clientY + 'px';
                inspectDiv.style.left = (e.clientX - 333) + 'px';
            });
        });
    }
};

/**
 * Adds an event listener to edit buttons that will fill the form with the row's data,
 * so the user can edit the record and submit.
 */
let updateListeners = () => {
    const updateButtons = document.querySelectorAll('span.update');

    for (let updateButton of updateButtons) {
        updateButton.addEventListener('click', (e) => {
            e.stopPropagation();

            let parentRow = e.target.closest('tr');
            let id = parentRow.dataset.id;
            let name = parentRow.dataset.name;
            let parts = parentRow.dataset.parts;

            document.getElementById('widget_id').value = id;
            document.getElementById('widget_name').value = name;
            document.getElementById('widget_parts').value = parts;
            document.getElementById('form_mode').value = 'update';
            document.querySelector('form#form_widget fieldset legend').innerHTML = 'Edit Widget #' + id;
            document.querySelector('form#form_widget fieldset button[type="submit"]').innerHTML = 'Edit Widget';
        });
    }
};

/**
 * Adds an event listener to delete buttons that send a request to delete the record
 * with the ID indicated in the row's dataset
 */
let deleteListeners = async () => {
    const deleteButtons = document.querySelectorAll('span.delete');

    for (let deleteButton of deleteButtons) {
        deleteButton.addEventListener('click', async (e) => {
            e.stopPropagation();

            let id = e.target.closest('tr').dataset.id;

            await fetch('/api/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: id})
            })
            .then((response) => response.json())
            .then((data) => populateTable(true));
        });
    }
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
                newRow.dataset[key] = row[key];
                rowClone.querySelector('td.' + key).innerHTML = row[key];
            }

            tbody.append(newRow);
        }

        inspectListeners();
        updateListeners();
        deleteListeners();
    });
};

/**
 * Handle close button for inspect div
 */
let inspectCloseListener = () => {
    let inspectDiv = document.querySelector('div#inspect');
    let inspectClose = inspectDiv.querySelector('div#inspect span.close');
    let inspectDivContent = inspectDiv.querySelector('span.content');

    inspectClose.addEventListener('click', (e) => {
        inspectDiv.classList.remove('show');
        inspectDivContent.innerHTML = '';
    });
};

window.onload = () => {
    formListener();
    populateTable();
    inspectCloseListener();
};
