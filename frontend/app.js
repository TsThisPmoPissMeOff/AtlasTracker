async function analyzeImages(bbox = null) {
    const input = document.getElementById("imageInput");
    const multi = document.getElementById("multiToggle").checked;
    const results = document.getElementById("results");

    if (!input.files.length) {
        alert("Please select at least one image.");
        return;
    }

    const formData = new FormData();

    if (multi) {
        // Multi-image mode
        for (let file of input.files) {
            formData.append("files", file);
        }
    } else {
        // Single-image mode
        formData.append("file", input.files[0]);
    }

    if (bbox) {
        formData.append("bbox", bbox);
    }

    results.innerHTML = "Analyzing…";

    try {
        const response = await fetch("https://YOUR_BACKEND_URL/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        results.innerHTML = "Error: " + err;
    }
}

function displayResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    if (!data.candidates || data.candidates.length === 0) {
        container.innerHTML = "<p>No candidates found.</p>";
        return;
    }

    data.candidates.forEach((c, i) => {
        const div = document.createElement("div");

        div.innerHTML = `
            <p><strong>Candidate ${i + 1}</strong></p>
            <p>Latitude: ${c.coords.lat.toFixed(5)}</p>
            <p>Longitude: ${c.coords.lon.toFixed(5)}</p>
            <p>Score: ${c.final_score.toFixed(3)}</p>

            <button onclick="openMap(${c.coords.lat}, ${c.coords.lon})">
                Open in Google Maps
            </button>

            <button onclick="refine(${c.coords.lat}, ${c.coords.lon})">
                Refine Location
            </button>

            <details>
                <summary>Explanation</summary>
                <pre>${JSON.stringify(data.explanation, null, 2)}</pre>
            </details>

            <hr>
        `;

        container.appendChild(div);
    });
}

function openMap(lat, lon) {
    window.open(`https://www.google.com/maps?q=${lat},${lon}`);
}

function refine(lat, lon) {
    const delta = 0.05;
    const bbox = `${lat - delta},${lon - delta},${lat + delta},${lon + delta}`;
    analyzeImages(bbox);
}

/* Enable multiple file selection dynamically */
document.getElementById("multiToggle").addEventListener("change", (e) => {
    const input = document.getElementById("imageInput");
    input.multiple = e.target.checked;
});
