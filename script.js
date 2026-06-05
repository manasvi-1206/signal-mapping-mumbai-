let map = L.map('map').setView([19.076, 72.877], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

let markers = [];

function clearMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

function signalColor(signal) {
    if (signal >= -79) return "green";
    if (signal >= -89) return "blue";
    if (signal >= -99) return "orange";
    return "red";
}

function renderTable(data, mode) {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";
    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.lat}</td>
            <td>${row.lng}</td>
            <td>${row.signal}</td>
            <td>${row.quality || ""}</td>
            <td>${row.radio || ""}</td>
            <td>${row.sim || ""}</td>
            <td>${row.points || (mode === 'dead' ? '-' : '')}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderSummary(data, mode) {
    const el = document.getElementById("summary");
    if (!data.length) {
        el.innerHTML = "No data found for this selection.";
        return;
    }
    if (mode === 'dead') {
        el.innerHTML = `<strong>Dead zones found:</strong> ${data.length}`;
        return;
    }
    const avg = data.reduce((s, r) => s + Number(r.signal || 0), 0) / data.length;
    el.innerHTML = `<strong>Total rows:</strong> ${data.length} | <strong>Average signal:</strong> ${avg.toFixed(2)} dBm`;
}

function renderMap(data, mode) {
    clearMarkers();
    data.forEach(row => {
        const isDead = mode === 'dead';
        const color = isDead ? "red" : signalColor(row.signal);
        const marker = L.circleMarker([row.lat, row.lng], {
            radius: isDead ? 10 : 6,
            color: color,
            fillColor: color,
            fillOpacity: isDead ? 0.6 : 0.85,
            weight: 2
        }).addTo(map).bindPopup(
            isDead
                ? `Dead Zone<br>Avg Signal: ${row.signal} dBm<br>Points: ${row.points || 1}`
                : `Signal: ${row.signal} dBm<br>Network: ${row.radio || ""}<br>Operator: ${row.sim || ""}`
        );
        markers.push(marker);
    });

    if (data.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.2));
    }
}

async function loadData(mode) {
    const operator = document.getElementById("operatorSelect").value;
    const res = await fetch(`/api/data?operator=${encodeURIComponent(operator)}&mode=${encodeURIComponent(mode)}`);
    const data = await res.json();
    renderSummary(data, mode);
    renderTable(data, mode);
    renderMap(data, mode);
    setTimeout(() => map.invalidateSize(), 200);
}