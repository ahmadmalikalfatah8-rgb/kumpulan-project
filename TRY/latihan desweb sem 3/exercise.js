const toggleButton = document.getElementById('toggleButton');
const targets = document.querySelectorAll('.highlight-target');

toggleButton.addEventListener('click', function() {
    targets.forEach(function(el) {
        el.classList.toggle('highlight');
    });

    if (toggleButton.textContent === 'Highlight Paragraf') {
        toggleButton.textContent = 'Hapus Highlight';
    } else {
        toggleButton.textContent = 'Highlight Paragraf';
    }
});