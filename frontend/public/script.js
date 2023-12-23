function uploadFile() {
    // функция которая получает файл пользователя и отправляет запрос на сервер
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
            renderTable(data);
        })
        .catch(error => {
            console.error('There was a problem with the upload:', error);
        });
    } else {
        console.log('Please select a file to upload.');
    }
};

function getRecordsFromDB() {
    // функция которая отправляет запрос на сервер и ренедерит таблицу с полученными данными
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
    // целочисленное деление
    return (val - val % by) / by;
};


function procesRecordsData(jsonData) {
    // функция которая обрабаывает данные с сервера и добавляет результаты по разряду и по классу 

    let prefix = div(jsonData[0].unid, 100);
    let newEnd = Object.assign({}, jsonData[jsonData.length-1]);
    newEnd.unid += 100;
    jsonData.push(newEnd);
    
    const len = jsonData.length;
    let curClass = jsonData[0].class_name;
    let result = [];
    let prefSum = {};
    let classSum = {};
    let totalSum = {};

    for (let key in jsonData[0]) {
        prefSum[key] = 0;
        totalSum[key] = 0;
        classSum[key] = 0;
    };

    result.push({type: 'class', description: curClass});
    for (i = 0; i < len; i++) { 
        record = jsonData[i];
        let newPrefix = div(record.unid, 100);

        if (((newPrefix != prefix))) {
            prefSum['unid'] = prefix;
            toAdd = Object.assign({}, prefSum);
            result.push(toAdd);
            prefix = newPrefix;
            
            for (let key in jsonData[0]) {
                classSum[key] += prefSum[key];
                prefSum[key] = 0;
            };
        };
        if (curClass != record.class_name) {
            curClass = record.class_name;
            classResultToAdd = Object.assign({}, classSum);
            classResultToAdd.unid = 'ПО КЛАССУ';
            result.push(classResultToAdd);
            result.push({type: 'class', description: curClass});
            
            for (let key in jsonData[0]) {
                totalSum[key] += classSum[key];
                classSum[key] = 0;
            };

        };

        for (let key in jsonData[0]) {
            prefSum[key] += record[key];
        };

        if (i != len-1) {
            result.push(record); 
        };
    };
    
    classResultToAdd = Object.assign({}, classSum);
    for (let key in jsonData[0]) {
        totalSum[key] += classResultToAdd[key];
    };
    classResultToAdd.unid = 'ПО КЛАССУ';
    totalSum.unid = "БАЛАНС"
    result.push(classResultToAdd);
    result.push(totalSum);
    return result
}

function renderTable(jsonData) {
    // функция которая создает таблицу с данными
    // присваивает тэгам различные классы, которые накладывают стили
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = ''; 

    jsonData.forEach(record => {
        let row = document.createElement('tr');

        if (record.type !== undefined) {
            const classNameCell = document.createElement('td');
            classNameCell.colSpan = 7;
            classNameCell.textContent = record.description;
            row.appendChild(classNameCell);
            row.classList.add('bold');
            row.classList.add('center');
        } else {
            if (record.unid < 100) {
                row.classList.add('bold');
            };
            if (record.unid === 'ПО КЛАССУ' || record.unid === "БАЛАНС") {
                row.classList.add('bolder');
            };          

            console.log(record.unid in ['ПО КЛАССУ', "БАЛАНС"])
            console.log(record.unid)
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
        };

        tableBody.appendChild(row);
    });

    document.getElementById('recordsTable').style.display = 'table';
}