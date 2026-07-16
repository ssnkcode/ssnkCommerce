/**
 * LolaShop - Catálogo de Juguetes
 * Main Application Script
 * 
 * Carga los productos DIRECTAMENTE desde products_final.json.
 * Si editás el JSON, refrescá la página y listo.
 */

(function() {
    'use strict';

    // =============================================
    // STATE
    // =============================================
    const state = {
        cart: JSON.parse(localStorage.getItem('lolashop_cart') || '[]'),
        activeCategory: 'all',
        searchQuery: '',
        sortBy: 'default',
        theme: localStorage.getItem('lolashop_theme') || 'light',
        mobileMenuOpen: false,
        cartOpen: false,
        modalOpen: false,
    };

    // =============================================
    // DATA - Se carga todo desde products_final.json
    // =============================================
    let PRODUCTS = [];
    let CATEGORIES = [];
    let CAT_EMOJI = {};

    const categoryEmojis = {
        'Drones': '🛸',
        'Vehículos': '🏎️',
        'Consolas': '🎮',
        'Proyectores': '🌟',
        'Audio': '🎧',
        'Fotografía': '📸',
        'Arte y Escritura': '🎨',
        'Pop It y Burbujas': '🫧',
        'Robots': '🤖',
        'Juegos de Rol': '👨‍⚕️',
        'Deportes': '⚽',
        'Juegos de Mesa': '🎲',
        'Peluches y Accesorios': '🧸',
        'Hogar y Decoración': '🏠',
        'Construcción': '🧱',
        'Otros': '✨',
    };

    const productEmojis = {
        'Drones': ['🛩️', '🛸', '🚁', '✈️'],
        'Vehículos': ['🏎️', '🚗', '🚙', '🚜'],
        'Consolas': ['🎮', '🕹️', '👾'],
        'Proyectores': ['🌟', '✨', '🔮', '💡'],
        'Audio': ['🎧', '🎤', '📻', '📞'],
        'Fotografía': ['📸', '📷', '🖨️'],
        'Arte y Escritura': ['🎨', '✏️', '🖊️', '🖍️', '🖊️', '🖌️'],
        'Pop It y Burbujas': ['🫧', '🫧', '🫧', '🔫'],
        'Robots': ['🤖', '🐕'],
        'Juegos de Rol': ['👩‍🍳', '💄', '👩‍⚕️', '🍳', '☕', '🧹', '👸'],
        'Deportes': ['⚽', '🏀', '🏐', '🛹'],
        'Juegos de Mesa': ['🎲', '♟️', '🧩', '🧠', '🎯', '🧮'],
        'Peluches y Accesorios': ['🧸', '🎒', '🔑', '👜', '🧸', '🎒', '🔑'],
        'Hogar y Decoración': ['🏠', '🧸', '🌈'],
        'Construcción': ['🧱', '🧲', '🏗️'],
        'Otros': ['✨', '📦', '🎪'],
    };

    // =============================================
    // LOAD DATA FROM JSON
    // =============================================
    async function loadProducts() {
        try {
            const res = await fetch('products_final.json?' + Date.now());
            if (!res.ok) throw new Error('HTTP ' + res.status);
            const data = await res.json();
            PRODUCTS = data.products || [];

            // Derivar categorías y emojis del JSON
            const catSet = new Set(PRODUCTS.map(p => p.category));
            CATEGORIES = [...catSet].sort();
            CAT_EMOJI = {};
            CATEGORIES.forEach(cat => {
                CAT_EMOJI[cat] = categoryEmojis[cat] || '📦';
            });
        } catch (e) {
            console.error('Error cargando products_final.json:', e);
            PRODUCTS = [];
            CATEGORIES = [];
            CAT_EMOJI = {};
        }

        // Renderizar después de cargar
        renderCategories();
        renderFilterButtons();
        renderProducts();
        updateCartUI();
    }

    function getProductEmoji(product) {
        const emojis = productEmojis[product.category] || ['📦'];
        const idx = (product.id - 1) % emojis.length;
        return emojis[idx];
    }

    // =============================================
    // DOM REFS
    // =============================================
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const els = {
        header: $('#header'),
        themeToggle: $('#themeToggle'),
        themeIcon: null,
        cartBtn: $('#cartBtn'),
        cartCount: $('#cartCount'),
        menuBtn: $('#menuBtn'),
        mobileNav: $('#mobileNav'),
        cartOverlay: $('#cartOverlay'),
        cartSidebar: $('#cartSidebar'),
        cartClose: $('#cartClose'),
        cartBody: $('#cartBody'),
        cartFooter: $('#cartFooter'),
        sendWhatsApp: $('#sendWhatsApp'),
        clearCart: $('#clearCart'),
        searchInput: $('#searchInput'),
        searchClear: $('#searchClear'),
        sortSelect: $('#sortSelect'),
        categoriesGrid: $('#categoriesGrid'),
        productsGrid: $('#productsGrid'),
        catalogCount: $('#catalogCount'),
        catalogEmpty: $('#catalogEmpty'),
        backToTop: $('#backToTop'),
        modalOverlay: $('#modalOverlay'),
        modalBody: $('#modalBody'),
        modalClose: $('#modalClose'),
    };

    if (els.themeToggle) {
        els.themeIcon = els.themeToggle.querySelector('.theme-toggle__icon');
    }

    // =============================================
    // THEME
    // =============================================
    function setTheme(theme) {
        state.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('lolashop_theme', theme);
        if (els.themeIcon) {
            els.themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    function initTheme() {
        if (!localStorage.getItem('lolashop_theme')) {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            state.theme = prefersDark ? 'dark' : 'light';
        }
        setTheme(state.theme);
    }

    // =============================================
    // CATEGORIES
    // =============================================
    function renderCategories() {
        if (!els.categoriesGrid) return;

        const counts = {};
        PRODUCTS.forEach(p => {
            counts[p.category] = (counts[p.category] || 0) + 1;
        });

        els.categoriesGrid.innerHTML = CATEGORIES.map(cat => {
            const emoji = CAT_EMOJI[cat] || '📦';
            const count = counts[cat] || 0;
            const isActive = state.activeCategory === cat;
            return `
                <div class="category-card ${isActive ? 'active' : ''}" 
                     data-category="${cat}" 
                     role="listitem"
                     tabindex="0"
                     aria-pressed="${isActive}"
                     aria-label="${cat} - ${count} productos">
                    <span class="category-card__emoji" aria-hidden="true">${emoji}</span>
                    <div class="category-card__info">
                        <span class="category-card__name">${cat}</span>
                        <span class="category-card__count">${count} productos</span>
                    </div>
                </div>
            `;
        }).join('');

        els.categoriesGrid.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', () => {
                const cat = card.dataset.category;
                state.activeCategory = cat === state.activeCategory ? 'all' : cat;
                updateFilterButtons();
                renderCategories();
                renderProducts();
                document.getElementById('catalogo').scrollIntoView({ behavior: 'smooth' });
            });
            
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }

    // =============================================
    // FILTER BUTTONS
    // =============================================
    function renderFilterButtons() {
        const container = $('.catalog__filters');
        if (!container) return;

        let html = `<button class="filter-btn ${state.activeCategory === 'all' ? 'active' : ''}" 
                        data-category="all" aria-pressed="${state.activeCategory === 'all'}">Todos</button>`;
        
        CATEGORIES.forEach(cat => {
            const emoji = CAT_EMOJI[cat] || '📦';
            const isActive = state.activeCategory === cat;
            html += `<button class="filter-btn ${isActive ? 'active' : ''}" 
                         data-category="${cat}" aria-pressed="${isActive}">
                         ${emoji} ${cat}
                     </button>`;
        });

        container.innerHTML = html;

        container.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                state.activeCategory = btn.dataset.category;
                updateFilterButtons();
                renderCategories();
                renderProducts();
            });
        });
    }

    function updateFilterButtons() {
        $$('.filter-btn').forEach(btn => {
            const isActive = btn.dataset.category === state.activeCategory;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-pressed', isActive);
        });
    }

    // =============================================
    // PRODUCTS
    // =============================================
    function getFilteredProducts() {
        let filtered = [...PRODUCTS];

        if (state.activeCategory !== 'all') {
            filtered = filtered.filter(p => p.category === state.activeCategory);
        }

        if (state.searchQuery) {
            const query = state.searchQuery.toLowerCase();
            filtered = filtered.filter(p =>
                p.name.toLowerCase().includes(query) ||
                p.category.toLowerCase().includes(query) ||
                p.price.includes(query)
            );
        }

        switch (state.sortBy) {
            case 'name-asc':
                filtered.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'name-desc':
                filtered.sort((a, b) => b.name.localeCompare(a.name));
                break;
            case 'price-asc':
                filtered.sort((a, b) => a.priceNum - b.priceNum);
                break;
            case 'price-desc':
                filtered.sort((a, b) => b.priceNum - a.priceNum);
                break;
        }

        return filtered;
    }

    function renderProducts() {
        if (!els.productsGrid) return;

        const filtered = getFilteredProducts();

        if (els.catalogCount) {
            els.catalogCount.textContent = `Mostrando ${filtered.length} producto${filtered.length !== 1 ? 's' : ''}`;
        }

        if (filtered.length === 0) {
            els.productsGrid.innerHTML = '';
            if (els.catalogEmpty) els.catalogEmpty.hidden = false;
            return;
        }

        if (els.catalogEmpty) els.catalogEmpty.hidden = true;

        els.productsGrid.innerHTML = filtered.map(product => {
            const emoji = getProductEmoji(product);
            const imgPath = product.img || null;
            const wsHtml = product.wholesale && product.wholesale.length > 0 
                ? `<small>Desde ${product.wholesale[product.wholesale.length - 1].split(' ')[1]} (${product.wholesale[product.wholesale.length - 1].split(' ')[0]})</small>`
                : '';

            const imageHtml = imgPath
                ? `<img class="product-card__photo" src="${imgPath}" alt="${product.name}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><span class="product-card__emoji" aria-hidden="true" style="display:none">${emoji}</span>`
                : `<span class="product-card__emoji" aria-hidden="true">${emoji}</span>`;

            return `
                <article class="product-card animate-in" role="listitem" data-id="${product.id}">
                    <div class="product-card__image">
                        ${imageHtml}
                        <span class="product-card__category">${product.category}</span>
                    </div>
                    <div class="product-card__body">
                        <h3 class="product-card__name">${product.name}</h3>
                        <div class="product-card__price">
                            ${product.price}
                            ${wsHtml}
                        </div>
                    </div>
                    <div class="product-card__footer">
                        <button class="product-card__btn product-card__btn--detail" 
                                onclick="event.stopPropagation(); window.lolaShop.showDetail(${product.id})"
                                aria-label="Ver detalle de ${product.name}">
                            Detalle
                        </button>
                        <button class="product-card__btn product-card__btn--whatsapp" 
                                onclick="event.stopPropagation(); window.lolaShop.addToCart(${product.id})"
                                aria-label="Consultar ${product.name} por WhatsApp">
                            💬 Consultar
                        </button>
                    </div>
                </article>
            `;
        }).join('');

        els.productsGrid.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', () => {
                const id = parseInt(card.dataset.id);
                window.lolaShop.showDetail(id);
            });
        });
    }

    // =============================================
    // PRODUCT DETAIL MODAL
    // =============================================
    function showDetail(productId) {
        const product = PRODUCTS.find(p => p.id === productId);
        if (!product || !els.modalBody || !els.modalOverlay) return;

        const emoji = getProductEmoji(product);
        const imgPath = product.img || null;

        const modalImageHtml = imgPath
            ? `<img class="modal__photo" src="${imgPath}" alt="${product.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'"><span style="display:none" aria-hidden="true">${emoji}</span>`
            : `<span aria-hidden="true">${emoji}</span>`;
        
        let wholesaleHtml = '';
        if (product.wholesale && product.wholesale.length > 0) {
            wholesaleHtml = `
                <div class="modal__wholesale-title">Precios Mayoristas</div>
                <div class="modal__wholesale-list">
                    ${product.wholesale.map(ws => {
                        const parts = ws.split(' ');
                        return `
                            <div class="modal__wholesale-item">
                                <span class="modal__wholesale-qty">${parts[0]} unidades</span>
                                <span class="modal__wholesale-price">${parts[1]}</span>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }

        const wsForWhatsApp = product.wholesale && product.wholesale.length > 0
            ? product.wholesale.map(ws => `  ${ws}`).join('%0A')
            : 'Sin precios mayoristas disponibles';

        els.modalBody.innerHTML = `
            <div class="modal__image">
                ${modalImageHtml}
            </div>
            <div class="modal__body">
                <span class="modal__category">${product.category}</span>
                <h2 class="modal__name">${product.name}</h2>
                <div class="modal__price">
                    ${product.price}
                    <small>Precio unitario</small>
                </div>
                ${wholesaleHtml}
                <div class="modal__actions">
                    <a href="https://wa.me/5491100000000?text=Hola!%20Quiero%20consultar%20por%20el%20producto%20${encodeURIComponent(product.name)}%20a%20${encodeURIComponent(product.price)}%0APrecios%20mayoristas:%0A${wsForWhatsApp}"
                       class="btn btn--primary btn--full" target="_blank" rel="noopener"
                       aria-label="Consultar ${product.name} por WhatsApp">
                        📱 Consultar por WhatsApp
                    </a>
                    <button class="btn btn--outline btn--full" 
                            onclick="window.lolaShop.addToCart(${product.id})">
                        💬 Agregar a mi consulta
                    </button>
                </div>
            </div>
        `;

        els.modalOverlay.classList.add('open');
        els.modalOverlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        state.modalOpen = true;

        setTimeout(() => {
            const closeBtn = els.modalOverlay.querySelector('.modal__close');
            if (closeBtn) closeBtn.focus();
        }, 100);
    }

    function closeModal() {
        if (els.modalOverlay) {
            els.modalOverlay.classList.remove('open');
            els.modalOverlay.setAttribute('aria-hidden', 'true');
        }
        document.body.style.overflow = '';
        state.modalOpen = false;
    }

    // =============================================
    // CART
    // =============================================
    function addToCart(productId) {
        const product = PRODUCTS.find(p => p.id === productId);
        if (!product) return;

        if (!state.cart.find(item => item.id === productId)) {
            state.cart.push({
                id: product.id,
                name: product.name,
                price: product.price
            });
            saveCart();
            updateCartUI();
            showToast(`${product.name} agregado a tu consulta`);
        } else {
            showToast('Este producto ya está en tu consulta');
        }
    }

    function removeFromCart(productId) {
        state.cart = state.cart.filter(item => item.id !== productId);
        saveCart();
        updateCartUI();
    }

    function clearCartItems() {
        state.cart = [];
        saveCart();
        updateCartUI();
    }

    function saveCart() {
        localStorage.setItem('lolashop_cart', JSON.stringify(state.cart));
    }

    function updateCartUI() {
        const count = state.cart.length;
        
        if (els.cartCount) {
            els.cartCount.textContent = count;
            els.cartCount.classList.toggle('visible', count > 0);
        }

        if (els.cartBody) {
            if (count === 0) {
                els.cartBody.innerHTML = `
                    <div class="cart-sidebar__empty">
                        <span aria-hidden="true">💬</span>
                        <p>Agregá productos para hacer tu consulta por WhatsApp</p>
                    </div>
                `;
                if (els.cartFooter) els.cartFooter.hidden = true;
            } else {
                els.cartBody.innerHTML = state.cart.map(item => `
                    <div class="cart-item">
                        <span class="cart-item__name">${item.name}</span>
                        <span class="cart-item__price">${item.price}</span>
                        <button class="cart-item__remove" 
                                onclick="window.lolaShop.removeFromCart(${item.id})"
                                aria-label="Quitar ${item.name}">
                            ✕
                        </button>
                    </div>
                `).join('');
                if (els.cartFooter) els.cartFooter.hidden = false;
            }
        }
    }

    function openCart() {
        if (els.cartOverlay) els.cartOverlay.classList.add('open');
        if (els.cartSidebar) {
            els.cartSidebar.classList.add('open');
            els.cartSidebar.setAttribute('aria-hidden', 'false');
        }
        document.body.style.overflow = 'hidden';
        state.cartOpen = true;
        if (els.cartBtn) els.cartBtn.setAttribute('aria-expanded', 'true');
    }

    function closeCart() {
        if (els.cartOverlay) els.cartOverlay.classList.remove('open');
        if (els.cartSidebar) {
            els.cartSidebar.classList.remove('open');
            els.cartSidebar.setAttribute('aria-hidden', 'true');
        }
        document.body.style.overflow = '';
        state.cartOpen = false;
        if (els.cartBtn) els.cartBtn.setAttribute('aria-expanded', 'false');
    }

    function sendWhatsAppMessage() {
        if (state.cart.length === 0) return;

        let message = 'Hola! Quiero hacer una consulta del catálogo LolaShop:%0A%0A';
        state.cart.forEach((item, i) => {
            message += `${i + 1}. ${item.name} - ${item.price}%0A`;
        });
        message += '%0AQuiero precios mayoristas y disponibilidad.';

        window.open(`https://wa.me/5491100000000?text=${message}`, '_blank');
    }

    // =============================================
    // TOAST NOTIFICATION
    // =============================================
    function showToast(message) {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%) translateY(20px);
            background: var(--text-primary);
            color: var(--bg-primary);
            padding: 12px 24px;
            border-radius: 9999px;
            font-size: 14px;
            font-weight: 500;
            z-index: 5000;
            opacity: 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            max-width: 90%;
            text-align: center;
            font-family: var(--font-sans);
        `;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(-50%) translateY(0)';
        });

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(-50%) translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    }

    // =============================================
    // MOBILE MENU
    // =============================================
    function toggleMobileMenu() {
        state.mobileMenuOpen = !state.mobileMenuOpen;
        if (els.mobileNav) {
            els.mobileNav.classList.toggle('open', state.mobileMenuOpen);
            els.mobileNav.setAttribute('aria-hidden', !state.mobileMenuOpen);
        }
        if (els.menuBtn) {
            els.menuBtn.classList.toggle('active', state.mobileMenuOpen);
            els.menuBtn.setAttribute('aria-expanded', state.mobileMenuOpen);
        }
    }

    // =============================================
    // SCROLL EFFECTS
    // =============================================
    function initScrollEffects() {
        window.addEventListener('scroll', () => {
            if (els.header) {
                els.header.classList.toggle('scrolled', window.scrollY > 10);
            }
            if (els.backToTop) {
                els.backToTop.classList.toggle('visible', window.scrollY > 400);
            }
        }, { passive: true });

        if (els.backToTop) {
            els.backToTop.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }
    }

    // =============================================
    // EVENT LISTENERS
    // =============================================
    function initEvents() {
        if (els.themeToggle) {
            els.themeToggle.addEventListener('click', () => {
                setTheme(state.theme === 'light' ? 'dark' : 'light');
            });
        }

        if (els.searchInput) {
            let searchTimeout;
            els.searchInput.addEventListener('input', () => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    state.searchQuery = els.searchInput.value.trim();
                    if (els.searchClear) {
                        els.searchClear.hidden = !state.searchQuery;
                    }
                    renderProducts();
                }, 200);
            });

            if (els.searchClear) {
                els.searchClear.addEventListener('click', () => {
                    els.searchInput.value = '';
                    state.searchQuery = '';
                    els.searchClear.hidden = true;
                    renderProducts();
                    els.searchInput.focus();
                });
            }
        }

        if (els.sortSelect) {
            els.sortSelect.addEventListener('change', () => {
                state.sortBy = els.sortSelect.value;
                renderProducts();
            });
        }

        if (els.cartBtn) els.cartBtn.addEventListener('click', openCart);
        if (els.cartClose) els.cartClose.addEventListener('click', closeCart);
        if (els.cartOverlay) els.cartOverlay.addEventListener('click', closeCart);
        if (els.sendWhatsApp) els.sendWhatsApp.addEventListener('click', sendWhatsAppMessage);
        if (els.clearCart) els.clearCart.addEventListener('click', () => {
            if (confirm('¿Limpiar tu lista de consulta?')) {
                clearCartItems();
            }
        });

        if (els.menuBtn) {
            els.menuBtn.addEventListener('click', toggleMobileMenu);
        }

        $$('.mobile-nav__link').forEach(link => {
            link.addEventListener('click', () => {
                state.mobileMenuOpen = false;
                if (els.mobileNav) els.mobileNav.classList.remove('open');
                if (els.menuBtn) els.menuBtn.classList.remove('active');
            });
        });

        if (els.modalClose) els.modalClose.addEventListener('click', closeModal);
        if (els.modalOverlay) {
            els.modalOverlay.addEventListener('click', (e) => {
                if (e.target === els.modalOverlay) closeModal();
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (state.modalOpen) closeModal();
                if (state.cartOpen) closeCart();
                if (state.mobileMenuOpen) toggleMobileMenu();
            }
        });

        $$('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    // =============================================
    // RESET FILTERS (global)
    // =============================================
    window.resetFilters = function() {
        state.activeCategory = 'all';
        state.searchQuery = '';
        if (els.searchInput) els.searchInput.value = '';
        if (els.searchClear) els.searchClear.hidden = true;
        updateFilterButtons();
        renderCategories();
        renderProducts();
    };

    // =============================================
    // PUBLIC API
    // =============================================
    window.lolaShop = {
        addToCart,
        removeFromCart,
        showDetail,
        resetFilters: window.resetFilters,
    };

    // =============================================
    // INIT
    // =============================================
    function init() {
        initTheme();
        loadProducts();      // <-- Carga TODO desde products_final.json
        initScrollEffects();
        initEvents();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
