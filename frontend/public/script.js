function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0]; 

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:8000/api/file/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json(); 
        })
        .then(data => {
            console.log('File uploaded successfully:', data);
        })
        .catch(error => {
            console.error('There was a problem with the upload:', error);
        });
    } else {
        console.log('Please select a file to upload.');
    }
};




function getRecordsFromDB() {
    fetch('http://127.0.0.1:8000/api/record/get', {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json(); 
    })
    .then(data => {
        console.log('File uploaded successfully:', data);
        renderTable(procesRecordsData(data));
    })
    .catch(error => {
        console.error('There was a problem with the upload:', error);
    });
};

function div(val, by){
    return (val - val % by) / by;
};




function procesRecordsData(jsonData) {
    let prefix = div(jsonData[0].unid, 100);
    const len = jsonData.length;
    let curClass = jsonData[0].class_name;
    let result = [];
    let prefSum = {};
    let classSum = {};
    let totalSum = {}
    for (let key in jsonData[0]) {
        prefSum[key] = 0;
        totalSum[key] = 0;
    };

    for (i = 0; i < len; i++) { 
        record = jsonData[i];
        let newPrefix = div(record.unid, 100);
        if (newPrefix != prefix) {
            prefSum['unid'] = prefix;
            result.push(Object.assign({}, prefSum));
            prefix = newPrefix;
            for (let key in jsonData[0]) {
                totalSum[key] += prefSum[key];
                prefSum[key] = 0;
            };
        } else {
            for (let key in jsonData[0]) {
                prefSum[key] += record[key];
                
            };
            console.log(prefSum);
        }

        if (curClass != record.class_name) {
            curClass = record.class_name;
            for (let key in jsonData[0]) {
                totalSum[key] += prefSum[key];
                prefSum[key] = 0; // доделать общую штуку для классов
            };
        }


        result.push(record);
    };
    result.push(totalSum);
    return result
}

function renderTable(jsonData) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = ''; // Clear the table body before rendering new data


    jsonData.forEach(record => {

        const row = document.createElement('tr');

        const idCell = document.createElement('td');
        idCell.textContent = record.unid;
        row.appendChild(idCell);

        const activeInCell = document.createElement('td');
        activeInCell.textContent = record.in_active_balance;
        row.appendChild(activeInCell);

        const passiveInCell = document.createElement('td');
        passiveInCell.textContent = record.in_passive_balance;
        row.appendChild(passiveInCell);

        const debitCell = document.createElement('td');
        debitCell.textContent = record.debit;
        row.appendChild(debitCell);

        const creditCell = document.createElement('td');
        creditCell.textContent = record.credit;
        row.appendChild(creditCell);

        const activeOutCell = document.createElement('td');
        activeOutCell.textContent = record.out_active_balance;
        row.appendChild(activeOutCell);

        const passiveOutCell = document.createElement('td');
        passiveOutCell.textContent = record.out_passive_balance;
        row.appendChild(passiveOutCell);

        tableBody.appendChild(row);
    });

    document.getElementById('recordsTable').style.display = 'table';
}