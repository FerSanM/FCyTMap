// JavaScript para ocultar la barra de desplazamiento después de un tiempo de inactividad
document.addEventListener('DOMContentLoaded', function () {
    const tableWrappers = document.querySelectorAll('.table-responsive');
    let timeoutId;

    function showScrollbar(tableWrapper) {
        tableWrapper.classList.remove('hide-scrollbar');
    }

    function hideScrollbar(tableWrapper) {
        tableWrapper.classList.add('hide-scrollbar');
    }

    function resetTimer() {
        tableWrappers.forEach(tableWrapper => showScrollbar(tableWrapper));
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            tableWrappers.forEach(tableWrapper => hideScrollbar(tableWrapper));
        }, 2000); // 2 segundos de inactividad
    }

    tableWrappers.forEach(tableWrapper => {
        tableWrapper.addEventListener('scroll', resetTimer);
    });
    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keydown', resetTimer);

    // Ocultar la barra de desplazamiento al cargar la página
    tableWrappers.forEach(tableWrapper => hideScrollbar(tableWrapper));
});