const express = require('express');

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/file/upload', (req, res) => {
    res.render('upload_file');
});

app.get('/record/get', (req, res) => {
    res.render('get_records');
});

app.listen(port, () => {
    console.log(`Сервер запущен на http://localhost:${port}`);
});