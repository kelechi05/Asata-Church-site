
// ===== MOBILE MENU =====
function toggleMenu() {
    document.getElementById("nav-links").classList.toggle("show");
}

// ===== DYNAMIC SLIDER =====
let currentIndex = 0;
const slides = document.getElementById("slides");
const totalSlides = document.querySelectorAll(".slide").length;

function updateSlide() {
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateSlide();
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateSlide();
}

// Auto slide every 5 seconds
setInterval(nextSlide, 5000);

// ===== Preacher YouTube Player =====
document.querySelectorAll("[data-youtube-player]").forEach((player) => {
    const trigger = player.querySelector("[data-youtube-src]");
    const iframe = player.querySelector("iframe");

    if (!trigger || !iframe) {
        return;
    }

    trigger.addEventListener("click", () => {
        iframe.src = trigger.dataset.youtubeSrc || iframe.dataset.src;
        player.classList.add("is-playing");
    });
});

// ===== Dynamic Year =====
document.getElementById("year").textContent = new Date().getFullYear();
