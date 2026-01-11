document.addEventListener('DOMContentLoaded', () => {

    /* =========================
       ТЕМА (dark / light)
    ========================= */

    const toggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const root = document.documentElement; // <-- html

    function setTheme(themeName) {
        localStorage.setItem('theme', themeName);
        root.setAttribute('data-theme', themeName);

        themeIcon.textContent = themeName === 'dark' ? '☀️' : '🌙';
    }

    // загрузка сохранённой темы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        root.setAttribute('data-theme', 'light');
    }

    // переключение
    toggleBtn.addEventListener('click', () => {
        const current = root.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        setTheme(next);
    });



    /* =========================
       КАТАЛОГ (поиск + показать ещё)
    ========================= */

    const searchInput = document.getElementById('searchInput');
    const allProducts = Array.from(document.querySelectorAll('.product-item'));
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const noResults = document.getElementById('noResults');

    let visibleCount = 6;
    const itemsPerLoad = 3;

    function renderCatalog() {
        const query = searchInput.value.toLowerCase().trim();
        let matches = 0;

        allProducts.forEach(product => {
            const title = product.dataset.title || '';
            const fandom = product.dataset.fandom || '';
            const tags = product.dataset.tags || '';

            const isMatch =
                !query ||
                title.includes(query) ||
                fandom.includes(query) ||
                tags.includes(query);

            if (isMatch) {
                matches++;
                if (matches <= visibleCount) {
                    product.classList.remove('d-none');
                } else {
                    product.classList.add('d-none');
                }
            } else {
                product.classList.add('d-none');
            }
        });

        loadMoreBtn.classList.toggle('d-none', matches <= visibleCount);
        noResults.classList.toggle('d-none', matches !== 0);
    }

    searchInput.addEventListener('input', () => {
        visibleCount = 6;
        renderCatalog();
    });

    loadMoreBtn.addEventListener('click', () => {
        visibleCount += itemsPerLoad;
        renderCatalog();
    });

    renderCatalog();
});



/* =========================
   Navbar scroll
========================= */

window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (!nav) return;

    nav.classList.toggle('navbar-scrolled', window.scrollY > 50);
});



/* =========================
   Закрытие мобильного меню
========================= */

const navLinks = document.querySelectorAll('.nav-link');
const menuToggle = document.getElementById('mainNav');

if (menuToggle && window.bootstrap) {
    const bsCollapse = new bootstrap.Collapse(menuToggle, { toggle: false });

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 992) {
                bsCollapse.hide();
            }
        });
    });
}
/* =========================
   Upload preview
========================= */

const refInput = document.getElementById("refImage");
const previewBox = document.getElementById("uploadPreview");
const previewImg = document.getElementById("previewImg");
const removeBtn = document.getElementById("removeImg");

if (refInput) {
  refInput.addEventListener("change", () => {
    const file = refInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = e => {
      previewImg.src = e.target.result;
      previewBox.classList.remove("d-none");
    };
    reader.readAsDataURL(file);
  });
}

if (removeBtn) {
  removeBtn.addEventListener("click", () => {
    refInput.value = "";
    previewImg.src = "";
    previewBox.classList.add("d-none");
  });
}
