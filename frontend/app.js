async function analyzeImage(bbox=null) {
    const fileInput = document.getElementById('imageInput');
    if(fileInput.files.length === 0) { alert("Select an image"); return; }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    if(bbox) formData.append("bbox", bbox);

    const response = await fetch("https://<YOUR_BACKEND_URL>/analyze", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    displayResults(data);
}

function displayResults(data){
    const div = document.getElementById('results');
    div.innerHTML = "";
    
    data.candidates.forEach((c, i) => {
        const btn = document.createElement('button');
        btn.innerText = `Open Candidate ${i+1} in Google Maps`;
        btn.onclick = () => window.open(`https://www.google.com/maps?q=${c.coords.lat},${c.coords.lon}`);
        
        const explanationDropdown = document.createElement('details');
        explanationDropdown.innerHTML = `<summary>Explanation</summary><pre>${JSON.stringify(data.explanation, null, 2)}</pre>`;
        
        div.appendChild(document.createTextNode(`Candidate ${i+1}: ${c.coords.lat},${c.coords.lon}, Score: ${c.final_score.toFixed(2)}`));
        div.appendChild(btn);
        div.appendChild(explanationDropdown);
        div.appendChild(document.createElement('hr'));
    });
}
