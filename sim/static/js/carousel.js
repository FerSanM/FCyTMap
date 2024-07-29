document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los contenedores de carrusel en la página
    let carousels = document.querySelectorAll(".carousel-container");

    carousels.forEach((carouselContainer) => {
        let carousel = carouselContainer.querySelector(".carousel");
        let items = carousel ? carousel.querySelectorAll(".item") : [];
        let dotsContainer = carouselContainer.querySelector(".dots");

        // Verifica si el contenedor de puntos y los ítems existen
        if (dotsContainer && items.length > 0) {
            // Limpia el contenedor de puntos por si ya tiene puntos de una inicialización anterior
            dotsContainer.innerHTML = '';

            // Insertar los puntos en el DOM
            items.forEach((_, index) => {
                let dot = document.createElement("span");
                dot.classList.add("dot");
                if (index === 0) dot.classList.add("active");
                dot.dataset.index = index;
                dotsContainer.appendChild(dot);
            });

            let dots = dotsContainer.querySelectorAll(".dot");

            // Función para mostrar un ítem específico
            function showItem(index) {
                items.forEach((item, idx) => {
                    item.classList.remove("active");
                    dots[idx].classList.remove("active");
                    if (idx === index) {
                        item.classList.add("active");
                        dots[idx].classList.add("active");
                    }
                });
            }

            // Event listeners para botones
            let prevButton = carouselContainer.querySelector(".prev");
            let nextButton = carouselContainer.querySelector(".next");

            if (prevButton) {
                prevButton.addEventListener("click", () => {
                    let index = [...items].findIndex((item) =>
                        item.classList.contains("active")
                    );
                    showItem((index - 1 + items.length) % items.length);
                });
            }

            if (nextButton) {
                nextButton.addEventListener("click", () => {
                    let index = [...items].findIndex((item) =>
                        item.classList.contains("active")
                    );
                    showItem((index + 1) % items.length);
                });
            }

            // Event listeners para puntos
            dots.forEach((dot) => {
                dot.addEventListener("click", () => {
                    let index = parseInt(dot.dataset.index);
                    showItem(index);
                });
            });
        }
    });
});
