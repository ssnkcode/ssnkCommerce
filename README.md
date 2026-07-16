# LolaShop - Catalogo Mayorista de Juguetes

Sitio web estatico para el catalogo mayorista de una polirubro y jugueteria argentina. Desarrollado sin frameworks ni dependencias, utilizando HTML, CSS y JavaScript puro.

## Estructura del proyecto

```
web/
├── index.html                  # Aplicacion de una sola pagina (SPA)
├── products_final.json         # Datos de 119 productos y 16 categorias
├── css/
│   └── style.css               # Estilos completos con temas claro/oscuro
├── js/
│   └── app.js                  # Logica de la aplicacion (IIFE vanilla JS)
├── juguetes/                   # Imagenes de productos (29 PNGs)
├── extract_pdf.py              # Extrae texto del catalogo PDF original
├── update_json.py              # Procesa PDF y genera products_final.json
├── generate_site.py            # Genera index.html y style.css desde JSON
└── LISTA DE JUGUETES - CT.1500 0.pdf (2).pdf   # Catalogo fuente PDF
```

## Funcionalidades

### Catalogo de productos
- 119 productos organizados en 16 categorias
- Busqueda en tiempo real (con debounce de 200ms)
- Filtrado por categoria desde la grilla o los botones de filtro
- Ordenamiento por nombre (A-Z / Z-A) y precio (mayor / menor)
- Tarjetas de producto con imagen, precio y boton de consulta por WhatsApp

### Tema claro/oscuro
- Toggle de tema con persistencia en `localStorage`
- Respeta la preferencia del sistema operativo (`prefers-color-scheme`)
- Variables CSS para todos los colores, sombras y transiciones

### Carrito de consultas
- Sidebar deslizante que recopila productos seleccionados
- Persistencia en `localStorage`
- Envio de la lista completa por WhatsApp con mensaje pre-armado

### Detalle de producto
- Modal con imagen ampliada, precio unitario y precios de mayoreo
- Boton de consulta directa por WhatsApp
- Boton para agregar al carrito de consultas

### Diseno responsive
- Enfoque mobile-first con breakpoints en 480px y 768px
- Menu hamburguesa para moviles
- Filtros con scroll horizontal en pantallas chicas
- Grid adaptativo de productos (1 a 4 columnas)

### Accesibilidad
- Navegacion por teclado (Escape cierra modales/menus)
- Atributos ARIA (`aria-label`, `aria-expanded`, `aria-live`, `role="dialog"`)
- Respeto a `prefers-reduced-motion` (deshabilita animaciones)
- Clases `sr-only` para contenido exclusivo de lectores de pantalla
- Estilos `:focus-visible` para indicadores de foco

### Extras
- Boton "volver arriba" al hacer scroll
- Imagenes con `loading="lazy"` y fallback a emoji
- Toast notifications para feedback de acciones
- Estilos optimizados para impresion (grilla de 2 columnas)

## Pipeline de datos

El contenido del catalogo se extrae de un PDF original mediante scripts de Python:

1. **`extract_pdf.py`** - Usa PyMuPDF (`fitz`) para extraer texto pagina por pagina del PDF
2. **`update_json.py`** - Procesa el texto extraido, mapea imagenes, categoriza productos y genera `products_final.json`
3. **`generate_site.py`** - Lee el JSON y genera el HTML y CSS del sitio

### Dependencias de Python
- `PyMuPDF` (`fitz`)

```bash
pip install PyMuPDF
```

## Datos de productos

Cada producto en `products_final.json` contiene:

```json
{
  "id": 1,
  "name": "DRONE AVION VELOCITY",
  "price": "$35.000",
  "priceNum": 35000.0,
  "wholesale": [],
  "category": "Drones",
  "page": 2,
  "img": "juguetes/drone_avion_velocity.png"
}
```

### Categorias

| Categoria | Cantidad | Emoji |
|-----------|----------|-------|
| Arte y Escritura | 30 | Palette |
| Peluches y Accesorios | 12 | Teddy Bear |
| Juegos de Mesa | 10 | Dado |
| Deportes | 8 | Balon |
| Pop It y Burbujas | 8 | Burbujas |
| Audio | 6 | Auriculares |
| Proyectores | 6 | Estrella |
| Construccion | 5 | Ladrillos |
| Drones | 5 | Ovni |
| Consolas | 4 | Control |
| Vehiculos | 4 | Auto |
| Juegos de Rol | 7 | Doctor |
| Robots | 2 | Robot |
| Fotografia | 2 | Camara |
| Hogar y Decoracion | 2 | Casa |
| Otros | 1 | Brillo |

Rango de precios: $2.000 a $85.000 (Pesos Argentinos).

## Uso local

No se necesita build ni servidor. Abrir `index.html` directamente en el navegador.

```bash
# Opcional: con Python
python -m http.server 8000
```

Luego acceder a `http://localhost:8000`.

## Stack tecnico

| Capa | Tecnologia |
|------|------------|
| Marcado | HTML5 |
| Estilos | CSS3 (Custom Properties, BEM) |
| Logica | JavaScript vanilla (ES6+) |
| Datos | JSON servido via `fetch()` |
| Fuentes | Google Fonts (Inter + Space Grotesk) |
| Pipeline | Python + PyMuPDF |

**No utiliza**: frameworks CSS, librerias JS, npm, bundlers, TypeScript, preprocessadores CSS, ni herramientas de build.

## Licencia

Proyecto privado. Todos los derechos reservados.
