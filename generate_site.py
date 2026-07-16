"""
LolaShop Catalog Generator
Generates a complete web catalog from extracted PDF product data.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import re

WEB_DIR = r'C:\Users\ssnk\Desktop\img_lola\web'

# Load final cleaned data
with open(os.path.join(WEB_DIR, 'products_final.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']
categories = sorted(set(p['category'] for p in products))

# Fix some product names
name_fixes = {
    'Auto Stunt Car De': 'Auto Stunt Car Hombre Araña',
    'Auto A Control A Control': 'Auto A Control Remoto F1',
    'Auricular Labubu Con': 'Auricular Labubu Con Peluche',
    'Auricular Labubus 613A': 'Auricular Labubus 613A',
    'Cartuchera Pizarra': 'Cartuchera Pizarra Mágica',
    'Lapiz Impresión 3D': 'Lápiz Impresión 3D',
    'Maletín Arstístico': 'Maletín Artístico Metálico',
    'Set De Joyas Para Armar / Mariposa': 'Set De Joyas Mariposa',
    'Set De Joyas Para Armar / Rectangulo': 'Set De Joyas Rectángulo',
    'Pop It Pop It': 'Pop It',
    'Robot Labubu Que Baila': 'Robot Labubu Que Baila',
    'Muñeco Coleccionable Ia': 'Muñeco Coleccionable IA',
    'Cámara Infantil Cámara Infantil Summer Vacation Summer Vacation': 'Cámara Infantil Summer Vacation',
    'Mini Cámara Mini Cámara Impresora Portátil Impresora Portátil': 'Mini Cámara Impresora Portátil',
    'Burbujero Unicornio Burbujero Unicornio Bubble Gun M-9 Bubble Gun M-9': 'Burbujero Unicornio Bubble Gun M-9',
    'Burbujero Dinosaurio Burbujero Dinosaurio M-8': 'Burbujero Dinosaurio M-8',
    'Burbujero Unicornio Burbujero Unicornio Al-': 'Burbujero Unicornio AL-2033',
    'Burbujero Dinosaurio Burbujero Dinosaurio Blue H014 Blue H014': 'Burbujero Dinosaurio Blue H014',
    'Burbujero Grande Bubble Action Bubble Action': 'Burbujero Grande Bubble Action',
    'Velador Magnético Velador Magnético Labubu / Capibara': 'Velador Magnético Labubu / Capibara',
    'Velador Capibara Velador Capibara Con Sacapunta': 'Velador Capibara Con Sacapunta',
    'Reloj Proyector Reloj Proyector Labubu / Capibara': 'Reloj Proyector Labubu / Capibara',
    'Dinosaurio Para Dinosaurio Para Desarmar Juguete': 'Dinosaurio Para Desarmar',
    'Mini Mesa De Mini Mesa De Pool': 'Mini Mesa De Pool',
    'Pelota De Futbol N5 Pelota De Futbol N5': 'Pelota De Fútbol N5',
    'Pelota Mundial Eco Pelota Mundial Eco - N 5': 'Pelota Mundial Eco N5',
    'Pelota De Futbol N2 Pelota De Futbol N2': 'Pelota De Fútbol N2',
    'Decoración Fluor Decoración Fluor Grande': 'Decoración Fluor Grande',
    'Decoración Fluor Decoración Fluor Pequeña 3D': 'Decoración Fluor Pequeña 3D',
    'Licuadora De Licuadora De Juguete Home': 'Licuadora De Juguete',
    'Cafetera De Cafetera De Juguete Home': 'Cafetera De Juguete',
    'Aspiradora De Juguete Home': 'Aspiradora De Juguete',
    'Juego Electrónico Juego Electrónico Russia Block': 'Juego Electrónico Russia Block',
    'Llavero Sorpresa Llavero Sorpresa Cry Baby': 'Llavero Sorpresa Cry Baby',
    'Llavero Peluche Llavero Peluche Capibara': 'Llavero Peluche Capibara',
    'Llavero Peluche Llavero Peluche Cry Baby': 'Llavero Peluche Cry Baby',
    'Mini Maquina Mini Maquina Saca Peluche': 'Mini Máquina Saca Peluche',
    'Peluche Con Manta Peluche Con Manta Labubu Y Capibara': 'Peluche Con Manta Labubu / Capibara',
    'Peluche Con Peluche Con Toalla': 'Peluche Con Toalla',
    'Pelota Inflable Pelota Inflable Pelota Inflable Peluche': 'Pelota Inflable Peluche',
    'Proyector Star Proyector Star Máster': 'Proyector Star Máster',
    'Auricular Cat Y47': 'Auriculares Cat Y47',
    'Walkie Talkie Walkie Talkie Infantil E-366': 'Walkie Talkie Infantil E-366',
    'Walkie Talkie Walkie Talkie Infantil': 'Walkie Talkie Infantil',
    'Joystick Ps4 Sony / Joystick Ps4 Sony / Argentina': 'Joystick PS4 Sony / Argentina',
    'Joystick Ps4 / Joystick Ps4 / Sony Liso': 'Joystick PS4 Sony Liso',
    'Microfono Parlante Microfono Parlante Microfono Parlante': 'Micrófono Parlante',
    'Monopoly Guerreras Kpop Guerreras Kpop': 'Monopoly Guerreras K-Pop',
    'Alfombra / Piso Didáctico Hexagonal X20 $21.700': 'Alfombra Piso Didáctico Hexagonal',
    'Alfombra / Piso Didáctico Triangular X20 $21.700': 'Alfombra Piso Didáctico Triangular',
    'Alfombra / Piso Didáctico Circular X20 $21.700': 'Alfombra Piso Didáctico Circular',
    'Alfombra De Goma De Bebé': 'Alfombra De Goma De Bebé',
    'Set De Fibras Glitter Dual Tip 12 Pcs': 'Set Fibras Glitter Dual Tip 12 Pcs',
    'Set De Fibras Glitter Dual Tip 24 Pcs': 'Set Fibras Glitter Dual Tip 24 Pcs',
    'Set De Arte Caracol Dream 46 Pcs': 'Set Arte Caracol Dream 46 Pcs',
    'Set De Arte 68Pcs': 'Set Arte 68 Pcs',
    'Set De Arte 168Pcs': 'Set Arte 168 Pcs',
    'Juego De Arte Diamond Paint 50X70': 'Juego Arte Diamond Paint 50x70',
    'Juego Didáctico Tarjeta Flash Dino': 'Juego Didáctico Tarjeta Flash Dino',
    'Diamond Paint Personajes 30X30Cm': 'Diamond Paint Personajes 30x30',
    'Diamond Paint Corazón Kc': 'Diamond Paint Corazón',
    'Diamond Paint Redondo Capibara': 'Diamond Paint Redondo Capibara',
    'Pizarra Mágica Animada 9"': 'Pizarra Mágica Animada 9"',
    'Pizarra Magica 12': 'Pizarra Mágica 12"',
    'Pizarra Magica Netmak Pequeña + Calculadora': 'Pizarra Mágica Netmak Pequeña + Calculadora',
    'Pizarra Magica Netmak': 'Pizarra Mágica Netmak',
    'Pizarra Magica 20 X 20 X 20 X 20 X 20': 'Pizarra Mágica 20x20',
    'Pizarra Magica 20 X 30 20 X 30 20 X 30': 'Pizarra Mágica 20x30',
    'Pizarra Mágica Animada 9\u201d': 'Pizarra Mágica Animada 9"',
    'Juguete Magnético 28 Pcs': 'Juguete Magnético 28 Pcs',
    'Juguete Magnético 48 Pcs': 'Juguete Magnético 48 Pcs',
    'Juguete Magnético 60 Pcs': 'Juguete Magnético 60 Pcs',
    'Juego Magnético - Modelo Varios': 'Juego Magnético Modelo Varios',
    'Juego De Suma': 'Juego De Suma',
    'Basketball Chico G': 'Basketball Chico',
    'Juego De Mente Line Up 4': 'Juego De Mente Line Up 4',
    'Rompecabezas Bombero Con Pizarra': 'Rompecabezas Bombero Con Pizarra',
    'Rompecabezas Infantil 60 Piezas 60 Piezas': 'Rompecabezas Infantil 60 Piezas',
    'Ajedrez 3 En 1': 'Ajedrez 3 En 1',
    'Tren Armador De Dominó': 'Tren Armador De Dominó',
    'Burbujero Delfín': 'Burbujero Delfín',
    'Pistola Burbujero Graffitti': 'Pistola Burbujero Graffiti',
    'Drone Avión': 'Drone Avión Velocity',
    'Set De Joyas Mariposa': 'Set De Joyas Mariposa',
    'Set De Joyas Rectángulo': 'Set De Joyas Rectángulo',
    'Lego Copa Mundial': 'Lego Copa Mundial',
    'Marcadores Touch- 24Pcs': 'Marcadores Touch 24 Pcs',
    'Marcadores Touch- 36Pcs': 'Marcadores Touch 36 Pcs',
    'Marcadores Touch- 48Pcs': 'Marcadores Touch 48 Pcs',
    'Marcadores Touch- 60Pcs': 'Marcadores Touch 60 Pcs',
    'Marcadores Touch- 80Pcs': 'Marcadores Touch 80 Pcs',
    'Marcadores Touch- 120Pcs': 'Marcadores Touch 120 Pcs',
    'Pelota Playera': 'Pelota Playera',
    'Juego De Mente': 'Juego De Mente',
}

# Fix duplicate drone names
drone_counter = 0
for p in products:
    if p['name'] in name_fixes:
        p['name'] = name_fixes[p['name']]
    
    # Handle duplicate "Drone Avión" entries
    if p['name'] == 'Drone Avión Velocity':
        drone_counter += 1
        if drone_counter == 1:
            p['name'] = 'Drone Avión Velocity'
        elif drone_counter == 2:
            p['name'] = 'Drone Avión Graffiti'

# Fix duplicate "Proyector Astronauta"
proj_count = 0
for p in products:
    if p['name'] == 'Proyector Astronauta':
        proj_count += 1
        if proj_count == 2:
            p['name'] = 'Proyector Astronauta Premium'

# Re-categorize after fixes
def categorize(name):
    n = name.lower()
    if 'dron' in n or 'drone' in n:
        return 'Drones'
    if any(w in n for w in ['auto ', 'trepador', 'stunt car', 'remoto f1', 'tanque de']):
        return 'Vehículos'
    if any(w in n for w in ['consola', 'joystick']):
        return 'Consolas'
    if any(w in n for w in ['proyector', 'velador', 'reloj proyector']):
        return 'Proyectores'
    if any(w in n for w in ['auricular', 'walkie', 'micrófono']):
        return 'Audio'
    if any(w in n for w in ['cámara', 'camara', 'impresora portátil']):
        return 'Fotografía'
    if any(w in n for w in ['pizarra', 'cartuchera', 'lápiz', 'lapiz', 'marcador', 'fibras', 'set arte', 'set de arte', 'maletín art', 'diamond paint', 'joyas']):
        return 'Arte y Escritura'
    if any(w in n for w in ['pop it', 'burbujero', 'pistola burbuja']):
        return 'Pop It y Burbujas'
    if any(w in n for w in ['robot', 'perro robot']):
        return 'Robots'
    if any(w in n for w in ['maletín cocina', 'maletín maquillaje', 'maletín doctora', 'licuadora', 'cafetera', 'aspiradora', 'barbie']):
        return 'Juegos de Rol'
    if any(w in n for w in ['pelota', 'basketball', 'fútbol', 'futbol', 'monopatín']):
        return 'Deportes'
    if any(w in n for w in ['rompecabezas', 'juego de mente', 'ajedrez', 'suma', 'monopoly', 'russia block', 'didáctico', 'mini mesa', 'tren armador']):
        return 'Juegos de Mesa'
    if any(w in n for w in ['peluche', 'labubu', 'llavero', 'muñeco', 'cartera', 'mini máquina']):
        return 'Peluches y Accesorios'
    if any(w in n for w in ['alfombra', 'goma', 'decoración']):
        return 'Hogar y Decoración'
    if any(w in n for w in ['magnético', 'magnetico', 'lego']):
        return 'Construcción'
    return 'Otros'

for p in products:
    p['category'] = categorize(p['name'])

categories = sorted(set(p['category'] for p in products))

# Category emoji mapping
cat_emoji = {
    'Arte y Escritura': '🎨',
    'Audio': '🎧',
    'Construcción': '🧱',
    'Consolas': '🎮',
    'Deportes': '⚽',
    'Drones': '🛸',
    'Fotografía': '📸',
    'Hogar y Decoración': '🏠',
    'Juegos de Mesa': '🎲',
    'Juegos de Rol': '👨‍⚕️',
    'Otros': '✨',
    'Peluches y Accesorios': '🧸',
    'Pop It y Burbujas': '🫧',
    'Proyectores': '🌟',
    'Robots': '🤖',
    'Vehículos': '🏎️',
}

# Save final data
final_data = {
    'products': products,
    'categories': categories,
    'catEmoji': cat_emoji
}

with open(os.path.join(WEB_DIR, 'products_final.json'), 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f'Datos finales: {len(products)} productos en {len(categories)} categorías')
for cat in categories:
    count = sum(1 for p in products if p['category'] == cat)
    emoji = cat_emoji.get(cat, '📦')
    print(f'  {emoji} {cat}: {count}')

print('\nGenerando archivos web...')

# =============================================
# GENERATE HTML
# =============================================

products_json_js = json.dumps(products, ensure_ascii=False)
categories_json_js = json.dumps(categories, ensure_ascii=False)
cat_emoji_json_js = json.dumps(cat_emoji, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LolaShop - Catálogo de Juguetes | Polirubro</title>
    <meta name="description" content="Catálogo de juguetes mayoristas LolaShop. Drones, consolas, juguetes educativos y más al mejor precio.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="../logo_hermana.png">
</head>
<body>
    <!-- HEADER -->
    <header class="header" id="header">
        <div class="header__inner">
            <a href="#" class="header__logo" aria-label="LolaShop Inicio">
                <span class="header__logo-icon">🧸</span>
                <div class="header__logo-text">
                    <span class="header__brand">LolaShop</span>
                    <span class="header__tagline">Polirubro y Juguetería</span>
                </div>
            </a>
            
            <nav class="header__nav" aria-label="Navegación principal">
                <a href="#catalogo" class="header__nav-link active">Catálogo</a>
                <a href="#categorias" class="header__nav-link">Categorías</a>
                <a href="#contacto" class="header__nav-link">Contacto</a>
            </nav>
            
            <div class="header__actions">
                <button class="theme-toggle" id="themeToggle" aria-label="Cambiar tema" title="Cambiar entre modo claro y oscuro">
                    <span class="theme-toggle__icon" aria-hidden="true">🌙</span>
                    <span class="theme-toggle__track">
                        <span class="theme-toggle__thumb"></span>
                    </span>
                </button>
                
                <button class="header__cart-btn" id="cartBtn" aria-label="Ver carrito de consultas" aria-expanded="false">
                    <span class="header__cart-icon" aria-hidden="true">💬</span>
                    <span class="header__cart-count" id="cartCount" aria-live="polite">0</span>
                </button>
                
                <button class="header__menu-btn" id="menuBtn" aria-label="Abrir menú" aria-expanded="false">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </div>
    </header>

    <!-- MOBILE NAV -->
    <div class="mobile-nav" id="mobileNav" aria-hidden="true">
        <nav aria-label="Navegación móvil">
            <a href="#catalogo" class="mobile-nav__link">Catálogo</a>
            <a href="#categorias" class="mobile-nav__link">Categorías</a>
            <a href="#contacto" class="mobile-nav__link">Contacto</a>
        </nav>
    </div>

    <!-- HERO -->
    <section class="hero" id="hero">
        <div class="hero__bg">
            <div class="hero__shape hero__shape--1"></div>
            <div class="hero__shape hero__shape--2"></div>
            <div class="hero__shape hero__shape--3"></div>
        </div>
        <div class="hero__content">
            <p class="hero__badge">📦 Catálogo Mayorista 2025</p>
            <h1 class="hero__title">
                Los mejores <span class="hero__highlight">juguetes</span> al mejor precio
            </h1>
            <p class="hero__subtitle">
                Explora nuestro catálogo completo con más de {len(products)} productos. 
                Precios especiales por cantidad. Envíos a todo el país.
            </p>
            <div class="hero__actions">
                <a href="#catalogo" class="btn btn--primary btn--lg">
                    <span>Ver Catálogo</span>
                    <span aria-hidden="true">→</span>
                </a>
                <a href="#contacto" class="btn btn--outline btn--lg">
                    <span>Contactar</span>
                </a>
            </div>
            <div class="hero__stats">
                <div class="hero__stat">
                    <span class="hero__stat-num">{len(products)}+</span>
                    <span class="hero__stat-label">Productos</span>
                </div>
                <div class="hero__stat">
                    <span class="hero__stat-num">{len(categories)}</span>
                    <span class="hero__stat-label">Categorías</span>
                </div>
                <div class="hero__stat">
                    <span class="hero__stat-num">1500</span>
                    <span class="hero__stat-label">Código CT</span>
                </div>
            </div>
        </div>
    </section>

    <!-- CATEGORIES -->
    <section class="categories" id="categorias" aria-label="Categorías">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Explora por Categoría</h2>
                <p class="section-subtitle">Encuentra lo que buscas filtrando por tipo de producto</p>
            </div>
            <div class="categories__grid" id="categoriesGrid" role="list">
            </div>
        </div>
    </section>

    <!-- CATALOG -->
    <section class="catalog" id="catalogo" aria-label="Catálogo de productos">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Catálogo Completo</h2>
                <p class="section-subtitle">{len(products)} productos disponibles</p>
            </div>
            
            <!-- Search & Filters -->
            <div class="catalog__controls">
                <div class="search" role="search">
                    <span class="search__icon" aria-hidden="true">🔍</span>
                    <input 
                        type="search" 
                        class="search__input" 
                        id="searchInput" 
                        placeholder="Buscar productos..." 
                        aria-label="Buscar productos"
                        autocomplete="off"
                    >
                    <button class="search__clear" id="searchClear" aria-label="Limpiar búsqueda" hidden>✕</button>
                </div>
                
                <div class="catalog__filters" role="group" aria-label="Filtros">
                    <button class="filter-btn active" data-category="all" aria-pressed="true">
                        Todos
                    </button>
                </div>
                
                <div class="catalog__sort">
                    <label for="sortSelect" class="sr-only">Ordenar por</label>
                    <select id="sortSelect" class="sort-select" aria-label="Ordenar productos">
                        <option value="default">Ordenar por</option>
                        <option value="name-asc">Nombre A-Z</option>
                        <option value="name-desc">Nombre Z-A</option>
                        <option value="price-asc">Menor precio</option>
                        <option value="price-desc">Mayor precio</option>
                    </select>
                </div>
            </div>
            
            <div class="catalog__count" id="catalogCount" aria-live="polite">
                Mostrando {len(products)} productos
            </div>
            
            <!-- Products Grid -->
            <div class="catalog__grid" id="productsGrid" role="list" aria-label="Lista de productos">
            </div>
            
            <div class="catalog__empty" id="catalogEmpty" hidden>
                <span class="catalog__empty-icon" aria-hidden="true">🔎</span>
                <h3>No se encontraron productos</h3>
                <p>Intenta con otros términos de búsqueda o cambia el filtro.</p>
                <button class="btn btn--primary" onclick="resetFilters()">Ver todos los productos</button>
            </div>
        </div>
    </section>

    <!-- CONTACT -->
    <section class="contact" id="contacto" aria-label="Contacto">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">¿Questions?</h2>
                <p class="section-subtitle">Contactanos para precios mayoristas y envíos</p>
            </div>
            <div class="contact__grid">
                <div class="contact__card">
                    <span class="contact__card-icon" aria-hidden="true">📱</span>
                    <h3>WhatsApp</h3>
                    <p>Envianos un mensaje para consultas y pedidos</p>
                    <a href="https://wa.me/5491100000000?text=Hola!%20Quiero%20hacer%20un%20pedido%20del%20catálogo%20LolaShop" class="btn btn--primary" target="_blank" rel="noopener">
                        Enviar mensaje
                    </a>
                </div>
                <div class="contact__card">
                    <span class="contact__card-icon" aria-hidden="true">📧</span>
                    <h3>Email</h3>
                    <p>Consultas generales y pedidos especiales</p>
                    <a href="mailto:info@lolashop.com" class="btn btn--outline">
                        Enviar email
                    </a>
                </div>
                <div class="contact__card">
                    <span class="contact__card-icon" aria-hidden="true">🏪</span>
                    <h3>Visitanos</h3>
                    <p>Todos los días de 9 a 19 hs</p>
                    <span class="contact__address">Av. Principal 1234</span>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <div class="footer__inner">
                <div class="footer__brand">
                    <span class="footer__logo">🧸 LolaShop</span>
                    <p>Polirubro y Juguetería - Catálogo Mayorista CT.1500</p>
                </div>
                <div class="footer__copy">
                    <p>&copy; 2025 LolaShop. Todos los derechos reservados.</p>
                    <p class="footer__note">Precios sujetos a cambio sin previo aviso. Stock sujeto a disponibilidad.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- CART SIDEBAR -->
    <div class="cart-overlay" id="cartOverlay" aria-hidden="true"></div>
    <aside class="cart-sidebar" id="cartSidebar" aria-label="Carrito de consultas" aria-hidden="true">
        <div class="cart-sidebar__header">
            <h2>Mi Consulta</h2>
            <button class="cart-sidebar__close" id="cartClose" aria-label="Cerrar carrito">✕</button>
        </div>
        <div class="cart-sidebar__body" id="cartBody">
            <div class="cart-sidebar__empty">
                <span aria-hidden="true">💬</span>
                <p>Agregá productos para hacer tu consulta por WhatsApp</p>
            </div>
        </div>
        <div class="cart-sidebar__footer" id="cartFooter" hidden>
            <button class="btn btn--primary btn--full" id="sendWhatsApp">
                <span>📱</span> Enviar consulta por WhatsApp
            </button>
            <button class="btn btn--outline btn--full" id="clearCart">
                Limpiar lista
            </button>
        </div>
    </aside>

    <!-- BACK TO TOP -->
    <button class="back-to-top" id="backToTop" aria-label="Volver arriba" hidden>
        <span aria-hidden="true">↑</span>
    </button>

    <!-- PRODUCT MODAL -->
    <div class="modal-overlay" id="modalOverlay" aria-hidden="true">
        <div class="modal" id="productModal" role="dialog" aria-modal="true" aria-label="Detalle del producto">
            <button class="modal__close" id="modalClose" aria-label="Cerrar detalle">✕</button>
            <div class="modal__body" id="modalBody"></div>
        </div>
    </div>

    <script>
        const PRODUCTS = {products_json_js};
        const CATEGORIES = {categories_json_js};
        const CAT_EMOJI = {cat_emoji_json_js};
    </script>
    <script src="js/app.js"></script>
</body>
</html>'''

os.makedirs(os.path.join(WEB_DIR, 'css'), exist_ok=True)
os.makedirs(os.path.join(WEB_DIR, 'js'), exist_ok=True)

with open(os.path.join(WEB_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print('  ✅ index.html generado')

# =============================================
# GENERATE CSS
# =============================================

css_content = r'''/* =============================================
   LolaShop - Catálogo de Juguetes
   CSS Variables + Light/Dark Theme
   ============================================= */

/* CSS Reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* Light Theme (default) */
:root,
[data-theme="light"] {
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f5f5f5;
    --bg-card: #ffffff;
    --bg-card-hover: #f8f8ff;
    --bg-input: #f0f0f0;
    --bg-badge: #f0e6ff;
    --bg-overlay: rgba(0, 0, 0, 0.5);

    --text-primary: #1a1a2e;
    --text-secondary: #4a4a6a;
    --text-tertiary: #8888a0;
    --text-inverse: #ffffff;
    --text-accent: #7c3aed;

    --border-primary: #e8e8f0;
    --border-hover: #c8c8e0;
    --border-accent: #7c3aed;

    --accent-primary: #7c3aed;
    --accent-secondary: #a78bfa;
    --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
    --accent-soft: rgba(124, 58, 237, 0.08);
    --accent-glow: rgba(124, 58, 237, 0.2);

    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 30px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.15);

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;

    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-display: 'Space Grotesk', 'Inter', sans-serif;

    --header-height: 72px;
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --transition-slow: 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* Dark Theme */
[data-theme="dark"] {
    --bg-primary: #0f0f1a;
    --bg-secondary: #1a1a2e;
    --bg-tertiary: #16162a;
    --bg-card: #1e1e35;
    --bg-card-hover: #252545;
    --bg-input: #252545;
    --bg-badge: rgba(124, 58, 237, 0.15);
    --bg-overlay: rgba(0, 0, 0, 0.7);

    --text-primary: #f0f0f5;
    --text-secondary: #b0b0c8;
    --text-tertiary: #6a6a88;
    --text-inverse: #1a1a2e;
    --text-accent: #a78bfa;

    --border-primary: #2a2a45;
    --border-hover: #3a3a5a;
    --border-accent: #a78bfa;

    --accent-primary: #7c3aed;
    --accent-secondary: #6d28d9;
    --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    --accent-soft: rgba(124, 58, 237, 0.12);
    --accent-glow: rgba(124, 58, 237, 0.3);

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.2);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 8px 30px rgba(0, 0, 0, 0.35);
    --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.5);
}

/* =============================================
   BASE STYLES
   ============================================= */

html {
    scroll-behavior: smooth;
    scroll-padding-top: var(--header-height);
}

body {
    font-family: var(--font-sans);
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    transition: background-color var(--transition-base), color var(--transition-base);
    -webkit-font-smoothing: antialiased;
}

.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

.sr-only {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0, 0, 0, 0); border: 0;
}

img { max-width: 100%; display: block; }
a { text-decoration: none; color: inherit; }

/* =============================================
   HEADER
   ============================================= */

.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    height: var(--header-height);
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-primary);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all var(--transition-base);
}

.header.scrolled {
    box-shadow: var(--shadow-md);
}

.header__inner {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}

.header__logo {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}

.header__logo-icon {
    font-size: 28px;
    line-height: 1;
}

.header__logo-text {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}

.header__brand {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 20px;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.header__tagline {
    font-size: 11px;
    color: var(--text-tertiary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.header__nav {
    display: none;
    gap: 4px;
}

@media (min-width: 768px) {
    .header__nav { display: flex; }
}

.header__nav-link {
    padding: 8px 16px;
    border-radius: var(--radius-full);
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all var(--transition-fast);
}

.header__nav-link:hover,
.header__nav-link.active {
    color: var(--text-accent);
    background: var(--accent-soft);
}

.header__actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Theme Toggle */
.theme-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-full);
    background: var(--bg-tertiary);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: 14px;
}

.theme-toggle:hover {
    border-color: var(--border-accent);
    background: var(--accent-soft);
}

.theme-toggle__icon {
    font-size: 16px;
    transition: transform var(--transition-base);
}

.theme-toggle__track {
    width: 36px;
    height: 20px;
    background: var(--border-primary);
    border-radius: 10px;
    position: relative;
    transition: background var(--transition-fast);
}

.theme-toggle__thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 16px;
    height: 16px;
    background: var(--bg-card);
    border-radius: 50%;
    transition: transform var(--transition-base);
    box-shadow: var(--shadow-sm);
}

[data-theme="dark"] .theme-toggle__track {
    background: var(--accent-primary);
}

[data-theme="dark"] .theme-toggle__thumb {
    transform: translateX(16px);
}

[data-theme="dark"] .theme-toggle__icon {
    transform: rotate(180deg);
}

/* Cart button */
.header__cart-btn {
    position: relative;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-md);
    background: var(--bg-tertiary);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: 18px;
}

.header__cart-btn:hover {
    border-color: var(--border-accent);
    background: var(--accent-soft);
}

.header__cart-count {
    position: absolute;
    top: -4px;
    right: -4px;
    min-width: 18px;
    height: 18px;
    padding: 0 5px;
    background: var(--accent-primary);
    color: white;
    font-size: 11px;
    font-weight: 700;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transform: scale(0.5);
    transition: all var(--transition-fast);
}

.header__cart-count.visible {
    opacity: 1;
    transform: scale(1);
}

/* Menu button (mobile) */
.header__menu-btn {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    width: 40px;
    height: 40px;
    padding: 10px;
    border: none;
    background: none;
    cursor: pointer;
}

.header__menu-btn span {
    display: block;
    width: 100%;
    height: 2px;
    background: var(--text-primary);
    border-radius: 2px;
    transition: all var(--transition-base);
}

@media (min-width: 768px) {
    .header__menu-btn { display: none; }
}

.header__menu-btn.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.header__menu-btn.active span:nth-child(2) { opacity: 0; }
.header__menu-btn.active span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Mobile Nav */
.mobile-nav {
    position: fixed;
    top: var(--header-height);
    left: 0;
    right: 0;
    z-index: 999;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-primary);
    padding: 16px 24px;
    transform: translateY(-100%);
    opacity: 0;
    transition: all var(--transition-slow);
    pointer-events: none;
}

.mobile-nav.open {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
}

.mobile-nav nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.mobile-nav__link {
    display: block;
    padding: 12px 16px;
    border-radius: var(--radius-md);
    font-weight: 500;
    font-size: 16px;
    color: var(--text-secondary);
    transition: all var(--transition-fast);
}

.mobile-nav__link:hover {
    background: var(--accent-soft);
    color: var(--text-accent);
}

/* =============================================
   HERO
   ============================================= */

.hero {
    position: relative;
    min-height: 85vh;
    display: flex;
    align-items: center;
    padding: calc(var(--header-height) + 60px) 24px 60px;
    overflow: hidden;
}

.hero__bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
}

.hero__shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.4;
}

.hero__shape--1 {
    width: 600px;
    height: 600px;
    background: var(--accent-primary);
    top: -200px;
    right: -100px;
    opacity: 0.15;
}

.hero__shape--2 {
    width: 400px;
    height: 400px;
    background: #f472b6;
    bottom: -100px;
    left: -100px;
    opacity: 0.1;
}

.hero__shape--3 {
    width: 300px;
    height: 300px;
    background: #06b6d4;
    top: 30%;
    left: 50%;
    opacity: 0.08;
}

.hero__content {
    position: relative;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.hero__badge {
    display: inline-block;
    padding: 8px 20px;
    background: var(--bg-badge);
    color: var(--text-accent);
    border-radius: var(--radius-full);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin-bottom: 24px;
    border: 1px solid var(--accent-glow);
}

.hero__title {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 20px;
    color: var(--text-primary);
}

.hero__highlight {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero__subtitle {
    font-size: clamp(1rem, 2vw, 1.2rem);
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 36px;
    line-height: 1.7;
}

.hero__actions {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 48px;
}

.hero__stats {
    display: flex;
    gap: 48px;
    justify-content: center;
    flex-wrap: wrap;
}

.hero__stat {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.hero__stat-num {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-accent);
    line-height: 1.2;
}

.hero__stat-label {
    font-size: 13px;
    color: var(--text-tertiary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* =============================================
   BUTTONS
   ============================================= */

.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: var(--radius-full);
    font-family: var(--font-sans);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
    border: 2px solid transparent;
    white-space: nowrap;
}

.btn--primary {
    background: var(--accent-gradient);
    color: white;
    border-color: var(--accent-primary);
    box-shadow: 0 2px 8px var(--accent-glow);
}

.btn--primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px var(--accent-glow);
}

.btn--outline {
    background: transparent;
    color: var(--text-accent);
    border-color: var(--border-accent);
}

.btn--outline:hover {
    background: var(--accent-soft);
}

.btn--sm {
    padding: 8px 16px;
    font-size: 12px;
}

.btn--lg {
    padding: 14px 32px;
    font-size: 16px;
}

.btn--full {
    width: 100%;
    justify-content: center;
}

/* =============================================
   SECTIONS
   ============================================= */

.section-header {
    text-align: center;
    margin-bottom: 48px;
}

.section-title {
    font-family: var(--font-display);
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    color: var(--text-primary);
}

.section-subtitle {
    font-size: 1rem;
    color: var(--text-tertiary);
}

/* =============================================
   CATEGORIES
   ============================================= */

.categories {
    padding: 80px 0;
}

.categories__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
}

.category-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 18px;
    background: var(--bg-card);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all var(--transition-fast);
    user-select: none;
}

.category-card:hover {
    border-color: var(--border-accent);
    background: var(--accent-soft);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.category-card.active {
    border-color: var(--accent-primary);
    background: var(--accent-soft);
    box-shadow: 0 0 0 3px var(--accent-glow);
}

.category-card__emoji {
    font-size: 24px;
    flex-shrink: 0;
    line-height: 1;
}

.category-card__info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.category-card__name {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.category-card__count {
    font-size: 11px;
    color: var(--text-tertiary);
}

/* =============================================
   CATALOG
   ============================================= */

.catalog {
    padding: 40px 0 80px;
    background: var(--bg-tertiary);
    transition: background-color var(--transition-base);
}

.catalog__controls {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
}

@media (min-width: 768px) {
    .catalog__controls {
        flex-direction: row;
        align-items: center;
    }
}

/* Search */
.search {
    position: relative;
    flex: 1;
    max-width: 400px;
}

.search__icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 16px;
    pointer-events: none;
    opacity: 0.5;
}

.search__input {
    width: 100%;
    padding: 12px 40px 12px 42px;
    background: var(--bg-card);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-full);
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-primary);
    transition: all var(--transition-fast);
    outline: none;
}

.search__input::placeholder {
    color: var(--text-tertiary);
}

.search__input:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-glow);
}

.search__clear {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: var(--bg-tertiary);
    color: var(--text-tertiary);
    border-radius: 50%;
    cursor: pointer;
    font-size: 12px;
    transition: all var(--transition-fast);
}

.search__clear:hover {
    background: var(--danger);
    color: white;
}

/* Filters */
.catalog__filters {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    flex: 1;
}

.filter-btn {
    padding: 8px 16px;
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-full);
    background: var(--bg-card);
    color: var(--text-secondary);
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
    white-space: nowrap;
}

.filter-btn:hover {
    border-color: var(--border-accent);
    color: var(--text-accent);
}

.filter-btn.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: white;
}

/* Sort */
.sort-select {
    padding: 10px 16px;
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-full);
    background: var(--bg-card);
    color: var(--text-primary);
    font-family: var(--font-sans);
    font-size: 13px;
    cursor: pointer;
    outline: none;
    transition: all var(--transition-fast);
    min-width: 160px;
}

.sort-select:focus {
    border-color: var(--accent-primary);
}

.catalog__count {
    font-size: 13px;
    color: var(--text-tertiary);
    margin-bottom: 20px;
    font-weight: 500;
}

/* Products Grid */
.catalog__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
}

/* Product Card */
.product-card {
    background: var(--bg-card);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all var(--transition-base);
    display: flex;
    flex-direction: column;
    cursor: pointer;
}

.product-card:hover {
    border-color: var(--border-accent);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.product-card__image {
    position: relative;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-tertiary);
    overflow: hidden;
}

.product-card__emoji {
    font-size: 64px;
    transition: transform var(--transition-slow);
}

.product-card:hover .product-card__emoji {
    transform: scale(1.15) rotate(-3deg);
}

.product-card__category {
    position: absolute;
    top: 12px;
    left: 12px;
    padding: 4px 10px;
    background: var(--bg-badge);
    color: var(--text-accent);
    border-radius: var(--radius-full);
    font-size: 11px;
    font-weight: 600;
}

.product-card__body {
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
}

.product-card__name {
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.product-card__price {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
    color: var(--accent-primary);
    letter-spacing: -0.02em;
}

.product-card__price small {
    font-size: 12px;
    font-weight: 400;
    color: var(--text-tertiary);
    display: block;
    margin-top: 2px;
}

.product-card__footer {
    padding: 14px 18px;
    border-top: 1px solid var(--border-primary);
    display: flex;
    gap: 8px;
}

.product-card__btn {
    flex: 1;
    padding: 10px;
    border-radius: var(--radius-md);
    font-family: var(--font-sans);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
    text-align: center;
}

.product-card__btn--detail {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-primary);
    color: var(--text-secondary);
}

.product-card__btn--detail:hover {
    border-color: var(--border-accent);
    color: var(--text-accent);
}

.product-card__btn--whatsapp {
    background: #25D366;
    border: 1px solid #25D366;
    color: white;
}

.product-card__btn--whatsapp:hover {
    background: #1fb855;
    transform: translateY(-1px);
}

/* Empty state */
.catalog__empty {
    text-align: center;
    padding: 80px 20px;
    color: var(--text-tertiary);
}

.catalog__empty-icon {
    font-size: 64px;
    display: block;
    margin-bottom: 16px;
}

.catalog__empty h3 {
    font-size: 1.25rem;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.catalog__empty p {
    margin-bottom: 24px;
}

/* =============================================
   PRODUCT MODAL
   ============================================= */

.modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 2000;
    background: var(--bg-overlay);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--transition-base);
}

.modal-overlay.open {
    opacity: 1;
    pointer-events: auto;
}

.modal {
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    max-width: 560px;
    width: 100%;
    max-height: 85vh;
    overflow-y: auto;
    position: relative;
    transform: translateY(20px) scale(0.98);
    transition: transform var(--transition-slow);
    box-shadow: var(--shadow-xl);
}

.modal-overlay.open .modal {
    transform: translateY(0) scale(1);
}

.modal__close {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-primary);
    border-radius: 50%;
    background: var(--bg-card);
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 16px;
    z-index: 10;
    transition: all var(--transition-fast);
}

.modal__close:hover {
    background: var(--danger);
    border-color: var(--danger);
    color: white;
}

.modal__image {
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-tertiary);
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.modal__image span {
    font-size: 100px;
}

.modal__body {
    padding: 28px;
}

.modal__category {
    display: inline-block;
    padding: 4px 12px;
    background: var(--bg-badge);
    color: var(--text-accent);
    border-radius: var(--radius-full);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 12px;
}

.modal__name {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-primary);
    line-height: 1.2;
}

.modal__price {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-primary);
    margin-bottom: 20px;
}

.modal__price small {
    font-size: 14px;
    font-weight: 400;
    color: var(--text-tertiary);
    display: block;
}

.modal__wholesale-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.modal__wholesale-title::before {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-primary);
}

.modal__wholesale-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 24px;
}

.modal__wholesale-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-primary);
}

.modal__wholesale-qty {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

.modal__wholesale-price {
    font-weight: 700;
    font-size: 16px;
    color: var(--accent-primary);
}

.modal__actions {
    display: flex;
    gap: 12px;
}

/* =============================================
   CONTACT
   ============================================= */

.contact {
    padding: 80px 0;
}

.contact__grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
}

.contact__card {
    text-align: center;
    padding: 40px 28px;
    background: var(--bg-card);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-xl);
    transition: all var(--transition-fast);
}

.contact__card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow-md);
}

.contact__card-icon {
    font-size: 40px;
    display: block;
    margin-bottom: 16px;
}

.contact__card h3 {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-primary);
}

.contact__card p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.contact__address {
    font-size: 14px;
    color: var(--text-accent);
    font-weight: 500;
}

/* =============================================
   FOOTER
   ============================================= */

.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-primary);
    padding: 32px 0;
    transition: all var(--transition-base);
}

.footer__inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    text-align: center;
}

@media (min-width: 768px) {
    .footer__inner {
        flex-direction: row;
        justify-content: space-between;
        text-align: left;
    }
}

.footer__logo {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 700;
}

.footer__brand p,
.footer__copy p {
    font-size: 13px;
    color: var(--text-tertiary);
}

.footer__note {
    margin-top: 4px;
    font-size: 11px !important;
    opacity: 0.7;
}

/* =============================================
   CART SIDEBAR
   ============================================= */

.cart-overlay {
    position: fixed;
    inset: 0;
    z-index: 3000;
    background: var(--bg-overlay);
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--transition-base);
}

.cart-overlay.open {
    opacity: 1;
    pointer-events: auto;
}

.cart-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 3001;
    width: 380px;
    max-width: 100%;
    background: var(--bg-card);
    border-left: 1px solid var(--border-primary);
    display: flex;
    flex-direction: column;
    transform: translateX(100%);
    transition: transform var(--transition-slow);
}

.cart-sidebar.open {
    transform: translateX(0);
}

.cart-sidebar__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-primary);
}

.cart-sidebar__header h2 {
    font-family: var(--font-display);
    font-size: 1.2rem;
    font-weight: 700;
}

.cart-sidebar__close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-primary);
    border-radius: 50%;
    background: none;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.cart-sidebar__close:hover {
    background: var(--danger);
    border-color: var(--danger);
    color: white;
}

.cart-sidebar__body {
    flex: 1;
    overflow-y: auto;
    padding: 16px 24px;
}

.cart-sidebar__empty {
    text-align: center;
    padding: 48px 16px;
    color: var(--text-tertiary);
}

.cart-sidebar__empty span {
    font-size: 48px;
    display: block;
    margin-bottom: 12px;
}

.cart-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-primary);
}

.cart-item__name {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    flex: 1;
    padding-right: 12px;
}

.cart-item__price {
    font-size: 13px;
    font-weight: 600;
    color: var(--accent-primary);
    white-space: nowrap;
}

.cart-item__remove {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: var(--bg-tertiary);
    color: var(--text-tertiary);
    border-radius: 50%;
    cursor: pointer;
    font-size: 10px;
    margin-left: 8px;
    transition: all var(--transition-fast);
}

.cart-item__remove:hover {
    background: var(--danger);
    color: white;
}

.cart-sidebar__footer {
    padding: 16px 24px;
    border-top: 1px solid var(--border-primary);
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* =============================================
   BACK TO TOP
   ============================================= */

.back-to-top {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 500;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-primary);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    box-shadow: var(--shadow-lg);
    transition: all var(--transition-fast);
    opacity: 0;
    transform: translateY(20px);
    pointer-events: none;
}

.back-to-top.visible {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
}

.back-to-top:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-xl);
}

/* =============================================
   ANIMATIONS
   ============================================= */

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-in {
    animation: fadeInUp 0.5s ease forwards;
    opacity: 0;
}

/* Stagger children */
.catalog__grid .product-card:nth-child(1) { animation-delay: 0.02s; }
.catalog__grid .product-card:nth-child(2) { animation-delay: 0.04s; }
.catalog__grid .product-card:nth-child(3) { animation-delay: 0.06s; }
.catalog__grid .product-card:nth-child(4) { animation-delay: 0.08s; }
.catalog__grid .product-card:nth-child(5) { animation-delay: 0.10s; }
.catalog__grid .product-card:nth-child(6) { animation-delay: 0.12s; }
.catalog__grid .product-card:nth-child(7) { animation-delay: 0.14s; }
.catalog__grid .product-card:nth-child(8) { animation-delay: 0.16s; }

/* =============================================
   RESPONSIVE
   ============================================= */

@media (max-width: 480px) {
    .hero {
        min-height: 75vh;
        padding-top: calc(var(--header-height) + 40px);
    }
    
    .hero__stats {
        gap: 24px;
    }
    
    .hero__stat-num {
        font-size: 1.5rem;
    }
    
    .catalog__grid {
        grid-template-columns: 1fr;
    }
    
    .categories__grid {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    }
    
    .modal {
        max-height: 95vh;
        border-radius: var(--radius-lg);
    }
}

@media (max-width: 768px) {
    .catalog__controls {
        flex-direction: column;
    }
    
    .search {
        max-width: 100%;
    }
    
    .catalog__filters {
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: 4px;
        -webkit-overflow-scrolling: touch;
    }
    
    .catalog__filters::-webkit-scrollbar {
        display: none;
    }
    
    .sort-select {
        width: 100%;
    }
}

@media print {
    .header, .hero, .categories, .contact, .footer,
    .back-to-top, .cart-sidebar, .cart-overlay,
    .modal-overlay, .catalog__controls, .product-card__footer {
        display: none !important;
    }
    
    .catalog {
        padding: 0;
        background: white;
    }
    
    .catalog__grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .product-card {
        break-inside: avoid;
    }
}

/* =============================================
   ACCESSIBILITY
   ============================================= */

:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    
    html {
        scroll-behavior: auto;
    }
}

/* =============================================
   SCROLLBAR
   ============================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--border-hover);
}
'''

with open(os.path.join(WEB_DIR, 'css', 'style.css'), 'w', encoding='utf-8') as f:
    f.write(css_content)

print('  ✅ css/style.css generado')

# =============================================
# GENERATE JAVASCRIPT
# =============================================

js_content = r'''/**
 * LolaShop - Catálogo de Juguetes
 * Main Application Script
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
    // PRODUCT EMOJI BY CATEGORY
    // =============================================
    const categoryEmojis = {
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

    function getProductEmoji(product) {
        const emojis = categoryEmojis[product.category] || ['📦'];
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
        // Check system preference
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

        // Event listeners
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

        // Category filter
        if (state.activeCategory !== 'all') {
            filtered = filtered.filter(p => p.category === state.activeCategory);
        }

        // Search filter
        if (state.searchQuery) {
            const query = state.searchQuery.toLowerCase();
            filtered = filtered.filter(p =>
                p.name.toLowerCase().includes(query) ||
                p.category.toLowerCase().includes(query) ||
                p.price.includes(query)
            );
        }

        // Sort
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

        // Update count
        if (els.catalogCount) {
            els.catalogCount.textContent = `Mostrando ${filtered.length} producto${filtered.length !== 1 ? 's' : ''}`;
        }

        // Empty state
        if (filtered.length === 0) {
            els.productsGrid.innerHTML = '';
            if (els.catalogEmpty) els.catalogEmpty.hidden = false;
            return;
        }

        if (els.catalogEmpty) els.catalogEmpty.hidden = true;

        els.productsGrid.innerHTML = filtered.map(product => {
            const emoji = getProductEmoji(product);
            const wsHtml = product.wholesale.length > 0 
                ? `<small>Desde ${product.wholesale[product.wholesale.length - 1].split(' ')[1]} (${product.wholesale[product.wholesale.length - 1].split(' ')[0]})</small>`
                : '';

            return `
                <article class="product-card animate-in" role="listitem" data-id="${product.id}">
                    <div class="product-card__image">
                        <span class="product-card__emoji" aria-hidden="true">${emoji}</span>
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

        // Click to open detail
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
        
        let wholesaleHtml = '';
        if (product.wholesale.length > 0) {
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

        const wsForWhatsApp = product.wholesale.length > 0
            ? product.wholesale.map(ws => `  ${ws}`).join('%0A')
            : 'Sin precios mayoristas disponibles';

        els.modalBody.innerHTML = `
            <div class="modal__image">
                <span aria-hidden="true">${emoji}</span>
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

        // Focus trap
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
        
        // Update count badge
        if (els.cartCount) {
            els.cartCount.textContent = count;
            els.cartCount.classList.toggle('visible', count > 0);
        }

        // Update sidebar
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
        // Remove existing toast
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
        // Header shadow on scroll
        window.addEventListener('scroll', () => {
            if (els.header) {
                els.header.classList.toggle('scrolled', window.scrollY > 10);
            }

            // Back to top
            if (els.backToTop) {
                els.backToTop.classList.toggle('visible', window.scrollY > 400);
            }
        }, { passive: true });

        // Back to top click
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
        // Theme toggle
        if (els.themeToggle) {
            els.themeToggle.addEventListener('click', () => {
                setTheme(state.theme === 'light' ? 'dark' : 'light');
            });
        }

        // Search
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

        // Sort
        if (els.sortSelect) {
            els.sortSelect.addEventListener('change', () => {
                state.sortBy = els.sortSelect.value;
                renderProducts();
            });
        }

        // Cart
        if (els.cartBtn) els.cartBtn.addEventListener('click', openCart);
        if (els.cartClose) els.cartClose.addEventListener('click', closeCart);
        if (els.cartOverlay) els.cartOverlay.addEventListener('click', closeCart);
        if (els.sendWhatsApp) els.sendWhatsApp.addEventListener('click', sendWhatsAppMessage);
        if (els.clearCart) els.clearCart.addEventListener('click', () => {
            if (confirm('¿Limpiar tu lista de consulta?')) {
                clearCartItems();
            }
        });

        // Mobile menu
        if (els.menuBtn) {
            els.menuBtn.addEventListener('click', toggleMobileMenu);
        }

        // Close mobile nav on link click
        $$('.mobile-nav__link').forEach(link => {
            link.addEventListener('click', () => {
                state.mobileMenuOpen = false;
                if (els.mobileNav) els.mobileNav.classList.remove('open');
                if (els.menuBtn) els.menuBtn.classList.remove('active');
            });
        });

        // Modal close
        if (els.modalClose) els.modalClose.addEventListener('click', closeModal);
        if (els.modalOverlay) {
            els.modalOverlay.addEventListener('click', (e) => {
                if (e.target === els.modalOverlay) closeModal();
            });
        }

        // Keyboard: ESC closes modal/cart/menu
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (state.modalOpen) closeModal();
                if (state.cartOpen) closeCart();
                if (state.mobileMenuOpen) toggleMobileMenu();
            }
        });

        // Smooth scroll for anchor links
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
        renderCategories();
        renderFilterButtons();
        renderProducts();
        updateCartUI();
        initScrollEffects();
        initEvents();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
'''

with open(os.path.join(WEB_DIR, 'js', 'app.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)

print('  ✅ js/app.js generado')

print('\n🎉 ¡Proyecto LolaShop generado exitosamente!')
print(f'\n📁 Estructura de archivos:')
print(f'   web/')
print(f'   ├── index.html')
print(f'   ├── css/')
print(f'   │   └── style.css')
print(f'   ├── js/')
print(f'   │   └── app.js')
print(f'   ├── products_final.json')
print(f'   └── products_clean.json')
