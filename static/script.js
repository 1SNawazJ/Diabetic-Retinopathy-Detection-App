// script.js
// This function is called when the 'Predict' button is clicked
async function predict() {
    const imageUpload = document.getElementById('imageUpload');
    const resultDiv = document.getElementById('result');
    
    // Get the selected file from the input element
    const file = imageUpload.files[0];
    
    // Check if a file is selected
    if (!file) {
        resultDiv.innerHTML = 'Please select an image.';
        return;
    }
    
    // Create a FormData object to send the file to the server
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Send a POST request to the Flask server for prediction
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        // Parse the JSON response from the server
        const data = await response.json();
        
        // Check if the response contains an error
        if (data.error) {
            resultDiv.innerHTML = `Error: ${data.error}`;
        } else {
            // Display the prediction result
            resultDiv.innerHTML = `Prediction: ${data.prediction}`;
        }
    } catch (error) {
        console.error('Prediction error:', error);
        resultDiv.innerHTML = 'An error occurred during prediction.';
    }
}


