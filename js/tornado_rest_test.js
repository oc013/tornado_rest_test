/**
 * Quick HTML escape to avoid XSS
 * @todo review for improvement
 * @link https://stackoverflow.com/a/6234804
 * @param {mixed} value
 * @returns mixed
 */
let escapeHTML = (value) => {
    if (typeof value == "string") {
        value = value.replace(/[&<>'"]/g, tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag]))
    }

    return value;
};

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
            if ('error' in data) {
                showError(data['error'], e.target);
            } else {
                e.target.reset();
                populateTable(true);
            }
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
                let outputInspect = '';
                for (let element in data) {
                    outputInspect += element + ': ' + escapeHTML(data[element]) + '<br>';
                }

                showTooltip(outputInspect, (e.clientX - 333), e.clientY);
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
        closeTooltip();
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
                rowClone.querySelector('td.' + key).innerHTML = escapeHTML(row[key]);
            }

            tbody.append(newRow);
        }

        inspectListeners();
        updateListeners();
        deleteListeners();
    });
};

/**
 * Display the tooltip with the content and coordinates provided
 * @param {String} content
 * @param {int} x
 * @param {int} y
 */
let showTooltip = (content, x, y, error=0) => {
    let tooltipDiv = document.querySelector('div#tooltip');
    let tooltipDivContent = tooltipDiv.querySelector('span.content');

    tooltipDivContent.innerHTML = content;
    tooltipDiv.classList.add('show');
    if (error) {
        tooltipDiv.classList.add('error');
    } else {
        tooltipDiv.classList.remove('error');
    }
    tooltipDiv.style.left = x + 'px';
    tooltipDiv.style.top = y + 'px';
};

/**
 * Parses error messages from the API and displays them in the tooltip at the coordinates of the element
 * @param {Array} errorArray
 * @param {Object} element
 */
let showError = (errorArray, element) => {
    let outputError = '';
    for (let errorMessage of errorArray) {
        outputError += errorMessage + '<br>';
    }
    var position = element.getBoundingClientRect();

    showTooltip(outputError, position.right - 50, position.bottom - 50, 1);
};

/**
 * Close the tooltip and remove content
 */
let closeTooltip = () => {
    let tooltipDiv = document.querySelector('div#tooltip');
    let tooltipDivContent = tooltipDiv.querySelector('span.content');

    tooltipDiv.classList.remove('show', 'error');
    tooltipDivContent.innerHTML = '';
};

/**
 * Handle close button for tooltip div
 */
let tooltipCloseListener = () => {
    let tooltipClose = document.querySelector('div#tooltip span.close');

    tooltipClose.addEventListener('click', (e) => {
        closeTooltip();
    });
};

window.onload = () => {
    formListener();
    populateTable();
    tooltipCloseListener();
};
