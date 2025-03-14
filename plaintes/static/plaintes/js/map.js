   document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map', {
        zoomControl: false,
        attributionControl: false
    }).setView([48.8566, 2.3522], 13);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© CartoDB',
        maxZoom: 19
    }).addTo(map);

    function updateMap() {
        fetch('/api/plaintes/')
            .then(response => response.json())
            .then(data => {
                map.eachLayer(layer => layer instanceof L.Marker && map.removeLayer(layer));
                data.forEach(plainte => {
                    const color = plainte.statut === 'resolu' ? '#FFFFFF' : '#005CE6';
                    const marker = L.circleMarker([plainte.latitude, plainte.longitude], {
                        radius: 10 * plainte.priorite,
                        fillColor: color,
                        color: '#FFFFFF',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.7
                    }).addTo(map);
                    marker.bindPopup(`<b>${plainte.titre}</b><br>${plainte.statut}<br>Priorité: ${plainte.priorite}`);
                });
            });
    }

    updateMap();
    setInterval(updateMap, 3000); // Mise à jour toutes les 3 secondes
});