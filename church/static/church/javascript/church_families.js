document.querySelectorAll("[data-family-slider]").forEach((slider) => {
    const track = slider.querySelector(".family-slider-track");
    const slides = Array.from(slider.querySelectorAll(".family-slide"));
    let currentIndex = 0;

    if (!track || slides.length <= 1) {
        return;
    }

    function updateSlider() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    setInterval(() => {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider();
    }, 4500);
});
