document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');
    const classificationP = document.getElementById('classification');
    const uploadedImage = document.getElementById('uploaded-image'); 
    

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                classificationP.textContent = data.result;
                resultDiv.classList.remove('hidden');

                // Set the uploaded image source and display it
                uploadedImage.src = URL.createObjectURL(formData.get('file')); // Get the uploaded file
                uploadedImage.style.display = 'block'; // Show the image
            } else {
                throw new Error('Server error');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while classifying the image.');
        }
    });
});