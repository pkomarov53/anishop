document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;

    // Функция установки темы
    function setTheme(themeName) {
        localStorage.setItem('theme', themeName);
        if (themeName === 'dark') {
            body.setAttribute('data-theme', 'dark');
            themeIcon.textContent = '☀️';
        } else {
            body.removeAttribute('data-theme');
            themeIcon.textContent = '🌙';
        }
    }

    // Проверка сохраненной темы при загрузке
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        setTheme('dark');
    } else {
        // Если темы нет в localStorage, можно проверить системные настройки
        // const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        // if (prefersDark) setTheme('dark');
    }

    // Обработчик клика
    toggleBtn.addEventListener('click', () => {
        if (body.getAttribute('data-theme') === 'dark') {
            setTheme('light');
        } else {
            setTheme('dark');
        }
    });
    document.addEventListener('DOMContentLoaded', () => {
    // --- ЛОГИКА КАТАЛОГА (ПОИСК + "ПОКАЗАТЬ ЕЩЁ") ---

    const searchInput = document.getElementById('searchInput');
    const productsContainer = document.getElementById('productsContainer');
    const allProducts = Array.from(document.querySelectorAll('.product-item'));
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const noResults = document.getElementById('noResults');

    let visibleCount = 6; // Сколько показывать сначала
    const itemsPerLoad = 3; // Сколько добавлять по кнопке

    // Функция отображения товаров
    function renderCatalog() {
        const query = searchInput.value.toLowerCase().trim();
        let matches = 0;
        let visibleMatches = 0;

        allProducts.forEach(product => {
            // Получаем данные из data-атрибутов
            const title = product.dataset.title;
            const fandom = product.dataset.fandom;
            const tags = product.dataset.tags;

            // Проверяем соответствие поиску (или если поиск пустой - true)
            const isMatch = !query ||
                            title.includes(query) ||
                            fandom.includes(query) ||
                            tags.includes(query);

            if (isMatch) {
                matches++;
                // Показываем только если мы не превысили лимит visibleCount
                if (matches <= visibleCount) {
                    product.classList.remove('d-none');
                    visibleMatches++;
                } else {
                    product.classList.add('d-none');
                }
            } else {
                product.classList.add('d-none');
            }
        });

        // Управление видимостью кнопки "Показать ещё"
        // Если количество совпадений больше, чем мы сейчас показали -> кнопка нужна
        if (matches > visibleCount) {
            loadMoreBtn.classList.remove('d-none');
        } else {
            loadMoreBtn.classList.add('d-none');
        }

        // Управление блоком "Ничего не найдено"
        if (matches === 0) {
            noResults.classList.remove('d-none');
        } else {
            noResults.classList.add('d-none');
        }
    }

    // Событие ввода в поиск
    searchInput.addEventListener('input', () => {
        // При поиске сбрасываем счетчик видимых до начального значения
        visibleCount = 6;
        renderCatalog();
    });

    // Событие клика "Показать ещё"
    loadMoreBtn.addEventListener('click', () => {
        visibleCount += itemsPerLoad;
        renderCatalog();
    });

    // Инициализация при загрузке
    renderCatalog();
});
});

window.addEventListener('scroll', function() {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.classList.add('navbar-scrolled');
    } else {
        nav.classList.remove('navbar-scrolled');
    }
});

// Закрытие мобильного меню при клике на ссылку
const navLinks = document.querySelectorAll('.nav-link');
const menuToggle = document.getElementById('mainNav');
const bsCollapse = new bootstrap.Collapse(menuToggle, {toggle:false});
navLinks.forEach((l) => {
    l.addEventListener('click', () => {
        if(window.innerWidth < 992) { bsCollapse.hide(); }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // --- ЛОГИКА КАТАЛОГА (ПОИСК + "ПОКАЗАТЬ ЕЩЁ") ---

    const searchInput = document.getElementById('searchInput');
    const productsContainer = document.getElementById('productsContainer');
    const allProducts = Array.from(document.querySelectorAll('.product-item'));
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const noResults = document.getElementById('noResults');

    let visibleCount = 6; // Сколько показывать сначала
    const itemsPerLoad = 3; // Сколько добавлять по кнопке

    // Функция отображения товаров
    function renderCatalog() {
        const query = searchInput.value.toLowerCase().trim();
        let matches = 0;
        let visibleMatches = 0;

        allProducts.forEach(product => {
            // Получаем данные из data-атрибутов
            const title = product.dataset.title;
            const fandom = product.dataset.fandom;
            const tags = product.dataset.tags;

            // Проверяем соответствие поиску (или если поиск пустой - true)
            const isMatch = !query ||
                            title.includes(query) ||
                            fandom.includes(query) ||
                            tags.includes(query);

            if (isMatch) {
                matches++;
                // Показываем только если мы не превысили лимит visibleCount
                if (matches <= visibleCount) {
                    product.classList.remove('d-none');
                    visibleMatches++;
                } else {
                    product.classList.add('d-none');
                }
            } else {
                product.classList.add('d-none');
            }
        });

        // Управление видимостью кнопки "Показать ещё"
        // Если количество совпадений больше, чем мы сейчас показали -> кнопка нужна
        if (matches > visibleCount) {
            loadMoreBtn.classList.remove('d-none');
        } else {
            loadMoreBtn.classList.add('d-none');
        }

        // Управление блоком "Ничего не найдено"
        if (matches === 0) {
            noResults.classList.remove('d-none');
        } else {
            noResults.classList.add('d-none');
        }
    }

    // Событие ввода в поиск
    searchInput.addEventListener('input', () => {
        // При поиске сбрасываем счетчик видимых до начального значения
        visibleCount = 6;
        renderCatalog();
    });

    // Событие клика "Показать ещё"
    loadMoreBtn.addEventListener('click', () => {
        visibleCount += itemsPerLoad;
        renderCatalog();
    });

    // Инициализация при загрузке
    renderCatalog();
});