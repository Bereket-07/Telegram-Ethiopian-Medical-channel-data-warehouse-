const baseURL = 'http://127.0.0.1:8000';

// Create a new detection
async function createDetection() {
    const detectionData = {
        filename: document.getElementById('filename').value,
        class_id: parseInt(document.getElementById('class_id').value),
        x_center: parseFloat(document.getElementById('x_center').value),
        y_center: parseFloat(document.getElementById('y_center').value),
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        confidence: parseFloat(document.getElementById('confidence').value)
    };

    await fetch(`${baseURL}/detections/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(detectionData)
    });
    alert("Detection Created!");
}

// Get all detections
async function getAllDetections() {
    const response = await fetch(`${baseURL}/detections/`);
    const detections = await response.json();

    const tbody = document.getElementById('detectionsTable').getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';
    detections.forEach(detection => {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = detection.id;
        row.insertCell(1).innerText = detection.filename;
        row.insertCell(2).innerText = detection.class_id;
        row.insertCell(3).innerHTML = `<button onclick="getDetectionById(${detection.id})">View</button>`;
    });
}

// Get detection by ID
async function getDetectionById(detectionId = null) {
    if (!detectionId) {
        detectionId = document.getElementById('detectionId').value;
    }
    const response = await fetch(`${baseURL}/detections/${detectionId}`);
    const detection = await response.json();

    const detailsSection = document.getElementById('detectionDetails');
    detailsSection.innerHTML = `
        <p>Filename: ${detection.filename}</p>
        <p>Class ID: ${detection.class_id}</p>
        <p>X Center: ${detection.x_center}</p>
        <p>Y Center: ${detection.y_center}</p>
        <p>Width: ${detection.width}</p>
        <p>Height: ${detection.height}</p>
        <p>Confidence: ${detection.confidence}</p>
    `;
}

// Update a detection by ID
async function updateDetection() {
    const detectionId = document.getElementById('updateId').value;
    const detectionData = {
        filename: document.getElementById('updateFilename').value,
        class_id: parseInt(document.getElementById('updateClassId').value),
        x_center: parseFloat(document.getElementById('updateXCenter').value),
        y_center: parseFloat(document.getElementById('updateYCenter').value),
        width: parseFloat(document.getElementById('updateWidth').value),
        height: parseFloat(document.getElementById('updateHeight').value),
        confidence: parseFloat(document.getElementById('updateConfidence').value)
    };

    await fetch(`${baseURL}/detections/${detectionId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(detectionData)
    });
    alert("Detection Updated!");
}

// Delete a detection by ID
async function deleteDetection() {
    const detectionId = document.getElementById('deleteId').value;
    await fetch(`${baseURL}/detections/${detectionId}`, {
        method: 'DELETE'
    });
    alert("Detection Deleted!");
}
