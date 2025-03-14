// Lazy loading des images
document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll("img[data-src]");
    const config = {
        rootMargin: "0px 0px 50px 0px",
        threshold: 0
    };

    let observer = new IntersectionObserver(function(entries, self) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.src = entry.target.dataset.src;
                self.unobserve(entry.target);
            }
        });
    }, config);

    images.forEach(image => observer.observe(image));
});