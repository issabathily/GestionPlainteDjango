document.addEventListener('DOMContentLoaded', () => {
    // Animation pour le glisser-déposer des photos
    const photoInput = document.querySelector('input[type="file"]');
    photoInput.addEventListener('dragover', (e) => e.preventDefault());
    photoInput.addEventListener('drop', (e) => {
        e.preventDefault();
        photoInput.files = e.dataTransfer.files;
    });

    // Filtrer les plaintes dynamiquement
    const filtreStatut = document.getElementById('filtre-statut');
    if (filtreStatut) {
        filtreStatut.addEventListener('change', () => {
            const statut = filtreStatut.value;
            document.querySelectorAll('#liste-plaintes li').forEach(li => {
                li.style.display = statut && !li.textContent.includes(statut) ? 'none' : 'block';
            });
        });
    }
});