function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0]; // Get the uploaded file

    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Send the file to the backend API using fetch
        let response = fetch('http://127.0.0.1:8000/file/upload', {
            method: 'POST',
            body: formData,
            mode: 'no-cors'
        });
        let commits = response.json();
        console.log(commits);
    //    .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok.');
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         // Handle the API response here
    //         console.log('File uploaded successfully:', data);
    //     })
    //     .catch(error => {
    //         // Handle errors
    //         console.error('There was a problem with the upload:', error);
    //     });
    } else {
        console.log('Please select a file to upload.');
    }
}
 