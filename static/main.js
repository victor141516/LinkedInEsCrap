document.addEventListener("DOMContentLoaded", function(event) {
    if (location.search === '?errorText') {
        document.getElementById('error-text').hidden = false;
    }
});
