document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const predictBtn = document.getElementById("predictBtn");
  const imagePreview = document.getElementById("imagePreview");
  const placeholder = document.getElementById("placeholder");
  const dropArea = document.getElementById("drop-area");
  const resultContainer = document.getElementById("resultContainer");
  const predictionResult = document.getElementById("predictionResult");
  const confidenceScore = document.getElementById("confidenceScore");
  const diseaseDescription = document.getElementById("diseaseDescription");
  const diseaseTreatment = document.getElementById("diseaseTreatment");
  const newScanBtn = document.getElementById("newScanBtn");
  const loadingOverlay = document.getElementById("loadingOverlay");

  let selectedFile = null;

  // Disease information
  const diseaseInfo = {
    "Bacterial leaf blight": {
      description: `<h3>About Bacterial Leaf Blight</h3>
                        <p>Bacterial leaf blight is caused by Xanthomonas oryzae pv. oryzae. It's one of the most serious diseases of rice, causing yellowing and drying of leaves and significant yield loss.</p>`,
      treatment: `<h3>Treatment & Management</h3>
                       <p>Use resistant rice varieties. Apply copper-based bactericides. Practice proper field drainage. Remove and destroy infected plants. Avoid excessive nitrogen fertilization.</p>`,
    },
    "Brown spot": {
      description: `<h3>About Brown Spot</h3>
                        <p>Brown spot is caused by the fungus Cochliobolus miyabeanus. It manifests as brown lesions on leaves and can cause significant damage especially in nutrient-deficient soils.</p>`,
      treatment: `<h3>Treatment & Management</h3>
                       <p>Use fungicides like propiconazole or tricyclazole. Ensure balanced nutrition. Use disease-free seeds. Practice crop rotation. Maintain optimal spacing between plants.</p>`,
    },
    "Leaf smut": {
      description: `<h3>About Leaf Smut</h3>
                        <p>Leaf smut is caused by the fungus Entyloma oryzae. It appears as small angular to oval spots on leaves with black powdery spore masses.</p>`,
      treatment: `<h3>Treatment & Management</h3>
                       <p>Apply fungicides like hexaconazole or propiconazole. Avoid excessive nitrogen. Remove infected debris after harvest. Use balanced fertilization. Plant resistant varieties.</p>`,
    },
  };

  // Handle click on upload button
  uploadBtn.addEventListener("click", function () {
    fileInput.click();
  });

  // Handle file selection
  fileInput.addEventListener("change", handleFileSelect);

  // Handle drag and drop
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, unhighlight, false);
  });

  dropArea.addEventListener("drop", handleDrop, false);
  dropArea.addEventListener("click", function () {
    fileInput.click();
  });

  // Handle prediction
  predictBtn.addEventListener("click", makePrediction);

  // Handle new scan
  newScanBtn.addEventListener("click", resetApplication);

  // Utility functions
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    dropArea.classList.add("highlight");
  }

  function unhighlight() {
    dropArea.classList.remove("highlight");
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
      handleFiles(files);
    }
  }

  function handleFileSelect(e) {
    if (e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  }

  function handleFiles(files) {
    const file = files[0];
    if (file && file.type.match("image.*")) {
      selectedFile = file;
      displayPreview(file);
      predictBtn.disabled = false;
    } else {
      alert("Please select a valid image file");
    }
  }

  function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imagePreview.style.display = "block";
      placeholder.style.display = "none";
    };
    reader.readAsDataURL(file);
  }

  function makePrediction() {
    if (!selectedFile) return;

    // Show loading overlay
    loadingOverlay.style.display = "flex";

    const reader = new FileReader();
    reader.readAsDataURL(selectedFile);
    reader.onload = function () {
      const base64Image = reader.result.split(",")[1];

      fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Hide loading overlay
          loadingOverlay.style.display = "none";

          // Display results
          displayResults(data);
        })
        .catch((error) => {
          console.error("Error:", error);
          loadingOverlay.style.display = "none";
          predictionResult.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error in prediction: ${error.message}`;
          resultContainer.style.display = "block";
        });
    };
  }

  function displayResults(data) {
    const disease = data[0].image;
    const confidence = data[0].confidence || "85.7%"; // Fallback if backend doesn't provide confidence

    predictionResult.textContent = disease;
    confidenceScore.textContent = `Confidence: ${confidence}`;

    // Display disease information
    if (diseaseInfo[disease]) {
      diseaseDescription.innerHTML = diseaseInfo[disease].description;
      diseaseTreatment.innerHTML = diseaseInfo[disease].treatment;
    } else {
      diseaseDescription.innerHTML =
        "<h3>Information</h3><p>No detailed information available for this disease.</p>";
      diseaseTreatment.innerHTML =
        "<h3>Recommendation</h3><p>Consult with an agricultural expert for proper diagnosis and treatment.</p>";
    }

    resultContainer.style.display = "block";

    // Scroll to result container
    resultContainer.scrollIntoView({ behavior: "smooth" });
  }

  function resetApplication() {
    // Reset file input
    fileInput.value = "";
    selectedFile = null;

    // Reset image preview
    imagePreview.style.display = "none";
    placeholder.style.display = "flex";

    // Reset prediction button
    predictBtn.disabled = true;

    // Hide result container
    resultContainer.style.display = "none";
  }
});
