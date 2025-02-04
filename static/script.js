let selectedFile = null;

// Handle image upload
document.getElementById("fileInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("imagePreview").src = e.target.result;
            document.getElementById("imagePreview").style.display = "block";
        };
        reader.readAsDataURL(file);
        document.getElementById("predictBtn").disabled = false;
    }
});

// Handle prediction request
document.getElementById("predictBtn").addEventListener("click", function() {
    if (!selectedFile) return;

    const formData = new FormData();
    const reader = new FileReader();
    reader.readAsDataURL(selectedFile);
    reader.onload = function() {
        formData.append("image", reader.result.split(',')[1]); 

        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: formData.get("image") })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("predictionResult").innerText = "Prediction: " + data[0].image;
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("predictionResult").innerText = "Error in prediction.";
        });
    };
});
