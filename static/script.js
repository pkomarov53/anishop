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