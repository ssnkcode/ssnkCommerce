import sys, io, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import fitz

WEB_DIR = r'C:\Users\ssnk\Desktop\img_lola\web'

# 1. Extract PDF data
pdf_path = os.path.join(WEB_DIR, 'LISTA DE JUGUETES - CT.1500 0.pdf (2).pdf')
doc = fitz.open(pdf_path)

pdf_products = []
for i, page in enumerate(doc):
    page_num = i + 1
    text = page.get_text()
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    if not lines:
        continue
    
    price_str = None
    name_lines = []
    
    for line in lines:
        cleaned = line.replace('|', '').strip()
        m = re.match(r'^\$[\d.,]+$', cleaned)
        if m:
            price_str = cleaned
        else:
            name_lines.append(line.strip())
    
    if not name_lines:
        continue
    
    name = ' '.join(name_lines)
    
    # Clean "Ct. 1500" / "CT. 1500" prefix
    name = re.sub(r'^(Ct\.\s*1500|CT\.\s*1500)\s*', '', name, flags=re.IGNORECASE).strip()
    
    # Clean "Ct.1500" suffix
    name = re.sub(r'\s*Ct\.1500$', '', name, flags=re.IGNORECASE).strip()
    
    price_clean = (price_str or '$0').replace('$', '').replace('.', '').replace(',', '').replace('|', '')
    try:
        price_num = float(price_clean)
    except:
        price_num = 0.0
    
    if price_num > 0 and name:
        pdf_products.append({
            'page': page_num,
            'name': name,
            'price': price_str or '$0',
            'priceNum': price_num
        })

# 2. Read current JSON to get wholesale and image data
json_path = os.path.join(WEB_DIR, 'products_final.json')
with open(json_path, 'r', encoding='utf-8') as f:
    current_data = json.load(f)

current_by_page = {}
for p in current_data['products']:
    current_by_page[p['page']] = p

# 3. Image mapping - comprehensive name to image
name_to_img = {
    'drone avión velocity': 'juguetes/drone_avion_velocity.png',
    'drone avión graffiti': 'juguetes/drone_avion_graffiti.png',
    'dron e88 pro': 'juguetes/drone_e88_pro.png',
    'dron d5 pro': 'juguetes/dron_d5_pro.png',
    'dron s5hp pro': 'juguetes/dron_s5hp_pro.png',
    'auto trepador': 'juguetes/auto_trepador.png',
    'perro robot stunt': 'juguetes/perro_robot.png',
    'auto stunt car de hombre araña': 'juguetes/auto_stunt_car_hombre_arana.png',
    'auto a control remoto f1': 'juguetes/auto_a_control_remoto_f1.png',
    'tanque de hidrogel': 'juguetes/tanque_de_hidrogel.png',
    'consola sup simple': 'juguetes/consola_sup_simple.png',
    'consola sup doble': 'juguetes/consola_sup_doble.png',
    'joystick ps4 sony / argentina': 'juguetes/joystick_ps4_sony_argentina.png',
    'joystick ps4 / sony liso': 'juguetes/joystick_ps4_sony_liso.png',
    'microfono parlante': 'juguetes/microfono_parlante.png',
    'proyector star máster': 'juguetes/proyector_star_master.png',
    'proyector astronauta': 'juguetes/proyector_astronauta.png',
    'auricular labubu con peluche': 'juguetes/auricular_labubu_con_peluche.png',
    'auriculares cat y47': 'juguetes/auriculares_cat_y47.png',
    'auricular labubus 613a': 'juguetes/auricular_labubus_613a.png',
    'walkie talkie infantil': 'juguetes/walkie_talkie_infantil.png',
    'walkie talkie infantil e-366': 'juguetes/walkie_talkie_infantil_e_366.png',
    'cámara infantil summer vacation': 'juguetes/camara_infantil_summer_vacation.png',
    'mini cámara impresora portátil': 'juguetes/mini_camara_impresora_portatil.png',
    'cartuchera pizarra mágica': 'juguetes/cartuchera_pizarra_magica.png',
    'pizarra mágica': 'juguetes/pizarra_magica.png',
    'pizarra magica 12″': 'juguetes/pizarra_magica_12.png',
    'pizarra mágica animada 9"': 'juguetes/PIZZARRA MAGICA ANIMADA 9.png',
    'pizarra mágica animada 9"': 'juguetes/PIZZARRA MAGICA ANIMADA 9.png',
    'pizarra magica netmak pequeña + calculadora': 'juguetes/pizarra_magica_netmak.png',
    'pizarra mágica netmak': 'juguetes/pizarra_magica_netmak.png',
    'lapiz impresión 3d': 'juguetes/lapiz_impresion_3d.png',
    'marcador para cerámica': 'juguetes/marcador_para_ceramica.png',
    'marcador para rostro': 'juguetes/marcador_para_rostro.png',
    'set de fibras glitter dual tip 12 pcs': 'juguetes/set_fibras_glitter_dual_tip_12_pcs.png',
    'set de fibras glitter dual tip 24 pcs': 'juguetes/set_fibras_glitter_dual_tip_24_pcs.png',
    'marcadores touch- 24pcs': 'juguetes/marcadores_touch_24_pcs.png',
    'marcadores touch- 36pcs': 'juguetes/marcadores_touch_36_pcs.png',
    'marcadores touch- 48pcs': 'juguetes/marcadores_touch_48_pcs.png',
    'marcadores touch- 60pcs': 'juguetes/marcadores_touch_60_pcs.png',
    'marcadores touch- 80pcs': 'juguetes/marcadores_touch_80_pcs.png',
    'marcadores touch- 120pcs': 'juguetes/marcadores_touch_120_pcs.png',
    'set de arte caracol dream 46 pcs': 'juguetes/set_arte_caracol_dream_46_pcs.png',
    'set de arte 68pcs': 'juguetes/set_arte_68_pcs.png',
    'set de arte 168pcs': 'juguetes/set_arte_168_pcs.png',
    'maletín arstístico metalico 145 pcs': 'juguetes/maletin_artistico_metalico_145_pcs.png',
    'set de joyas para armar / mariposa': 'juguetes/set_de_joyas_mariposa.png',
    'set de joyas para armar / rectangulo': 'juguetes/set_de_joyas_rectangulo.png',
    'diamond paint personajes 30x30cm': 'juguetes/diamond_paint_personajes_30x30.png',
    'juego de arte diamond paint 50x70': 'juguetes/juego_arte_diamond_paint_50x70.png',
    'diamond paint corazón kc1197': 'juguetes/diamond_paint_corazon.png',
    'diamond paint redondo capibara': 'juguetes/diamond_paint_redondo_capibara.png',
    'pop it princesa': 'juguetes/pop_it_princesa.png',
    'pop it astronauta': 'juguetes/pop_it_astronauta.png',
    'pop it jirafa': 'juguetes/pop_it_jirafa.png',
    'juego electrónico russia block': 'juguetes/juego_electronico_russia_block.png',
    'burbujero delfín': 'juguetes/burbujero_delfin.png',
    'burbujero unicornio al-2033': 'juguetes/burbujero_unicornio_al_2033.png',
    'burbujero unicornio bubble gun m-9': 'juguetes/burbujero_unicornio_bubble_gun_m_9.png',
    'burbujero dinosaurio m-8': 'juguetes/burbujero_dinosaurio.png',
    'pistola burbujero graffitti': 'juguetes/pistola_burbujero_graffiti.png',
    'burbujero dinosaurio blue h014': 'juguetes/burbujero_dinosaurio_blue_h014.png',
    'burbujero grande bubble action': 'juguetes/burbujero_grande_bubble_action.png',
    'velador magnético labubu / capibara': 'juguetes/velador_magnetico_labubu_capibara.png',
    'velador capibara con sacapunta': 'juguetes/velador_capibara_con_sacapunta.png',
    'robot labubu que baila': 'juguetes/robot_labubu_que_baila.png',
    'reloj proyector labubu / capibara': 'juguetes/reloj_proyector_labubu_capibara.png',
    'muñeco coleccionable ia': 'juguetes/muneco_coleccionable_ia.png',
    'maletín cocina': 'juguetes/maletin_cocina.png',
    'maletín maquillaje': 'juguetes/maletin_maquillaje.png',
    'maletín doctora': 'juguetes/maletin_doctora.png',
    'licuadora de juguete home': 'juguetes/licuadora_de_juguete.png',
    'cafetera de juguete home': 'juguetes/cafetera_de_juguete.png',
    'aspiradora de juguete home': 'juguetes/aspiradora_de_juguete.png',
    'barbie en moto': 'juguetes/barbie_en_moto.png',
    'tren armador de dominó': 'juguetes/tren_armador_de_domino.png',
    'pelota inflable peluche': 'juguetes/pelota_inflable_peluche.png',
    'pelota de básquet': 'juguetes/pelota_de_basquet.png',
    'pelota de voley': 'juguetes/pelota_de_voley.png',
    'pelota de futbol n5': 'juguetes/pelota_de_futbol_n5.png',
    'pelota mundial eco - n 5 318 gr': 'juguetes/pelota_mundial_eco_n5.png',
    'pelota de futbol n298 gr': 'juguetes/pelota_de_futbol_n2.png',
    'pelota playera': 'juguetes/pelota_playera.png',
    'decoración fluor grande': 'juguetes/decoracion_fluor_grande.png',
    'decoración fluor pequeña 3d': 'juguetes/decoracion_fluor_pequena_3d.png',
    'juego didáctico tarjeta flash dino': 'juguetes/juego_didactico_tarjeta_flash_dino.png',
    'monopoly guerreras kpop': 'juguetes/monopoly_guerreras_k_pop.png',
    'ajedrez 3 en 1': 'juguetes/ajedrez_3_en_1.png',
    'juego de suma': 'juguetes/juego_de_suma.png',
    'basketball chico g5027': 'juguetes/basketball_chico.png',
    'juego de mente line up 4': 'juguetes/juego_de_mente_line_up_4.png',
    'rompecabezas bombero con pizarra': 'juguetes/rompecabezas_bombero_con_pizarra.png',
    'rompecabezas zoológico': 'juguetes/rompecabezas_zoologico.png',
    'rompecabezas infantil 60 piezas': 'juguetes/rompecabezas_infantil_60_piezas.png',
    'juego magnético - modelo varios': 'juguetes/juego_magnetico_modelo_varios.png',
    'mini mesa de pool': 'juguetes/mini_mesa_de_pool.png',
    'dinosaurio para desarmar juguete': 'juguetes/dinosaurio_para_desarmar.png',
    'lego copa mundial': 'juguetes/lego_copa_mundial.png',
    'juguete magnético 28 pcs': 'juguetes/juguete_magnetico.png',
    'juguete magnético 48 pcs': 'juguetes/juguete_magnetico.png',
    'juguete magnético 60 pcs': 'juguetes/juguete_magnetico.png',
    'alfombra / piso didáctico hexagonal': 'juguetes/alfombra_piso_didactico_hexagonal.png',
    'alfombra / piso didáctico triangular': 'juguetes/alfombra_piso_didactico_triangular.png',
    'alfombra / piso didáctico circular': 'juguetes/alfombra_piso_didactico_circular.png',
    'alfombra de goma de bebé': 'juguetes/alfombra_de_goma_de_bebe.png',
    'cartera importada capibara': 'juguetes/cartera_importada_capibara.png',
    'llavero charm': 'juguetes/llavero_charm.png',
    'llavero sorpresa cry baby': 'juguetes/llavero_sorpresa_cry_baby.png',
    'llavero peluche capibara': 'juguetes/llavero_peluche.png',
    'llavero peluche cry baby': 'juguetes/llavero_peluche.png',
    'mini maquina saca peluche': 'juguetes/mini_maquina_saca_peluche.png',
    'peluche capibara pequeño': 'juguetes/peluche_capibara_pequeno.png',
    'peluche con manta labubu y capibara': 'juguetes/peluche_con_manta_labubu_capibara.png',
    'peluche con toalla': 'juguetes/peluche_con_toalla.png',
    'labubu gigante zimomo': 'juguetes/labubu_gigante_zimomo.png',
    'monopatín grafiti': 'juguetes/monopatin_grafiti.png',
    'auriculares gatito labubu inalambrico': None,  # No image
}

def find_image(name):
    n_lower = name.lower().strip()
    if n_lower in name_to_img:
        return name_to_img[n_lower]
    return None

# 4. Categories
def get_category(name):
    n = name.lower()
    if any(x in n for x in ['drone', 'dron ', 'avión']):
        return 'Drones'
    if any(x in n for x in ['auto ', 'trepador', 'stunt car', 'tanque', 'control remoto']):
        return 'Vehículos'
    if any(x in n for x in ['consola', 'joystick']):
        return 'Consolas'
    if any(x in n for x in ['micrófono', 'microfono', 'auricular', 'walkie', 'auriculares']):
        return 'Audio'
    if any(x in n for x in ['proyector', 'velador', 'reloj proyector']):
        return 'Proyectores'
    if any(x in n for x in ['cámara', 'camara', 'mini cámara']):
        return 'Fotografía'
    if any(x in n for x in ['pizarra', 'cartuchera', 'lapiz', 'lápiz', 'marcador', 'fibras', 'set de fibras', 'touch', 'set de arte', 'maletín artístico', 'maletín arstístico', 'diamond paint', 'juego de arte', 'rompecabezas']):
        return 'Arte y Escritura'
    if any(x in n for x in ['pop it', 'burbujero', 'pistola burbuja', 'bubble']):
        return 'Pop It y Burbujas'
    if any(x in n for x in ['robot', 'labubu que baila']):
        return 'Robots'
    if any(x in n for x in ['set de joyas']):
        return 'Arte y Escritura'
    if any(x in n for x in ['maletín cocina', 'maletín maquillaje', 'maletín doctora', 'licuadora', 'cafetera', 'aspiradora', 'barbie']):
        return 'Juegos de Rol'
    if any(x in n for x in ['pelota', 'básquet', 'basquet', 'voley', 'fútbol', 'futbol', 'playera', 'basketball', 'monopatín', 'inflable']):
        return 'Deportes'
    if any(x in n for x in ['tren armador', 'ajedrez', 'juego de suma', 'juego de mente', 'monopoly', 'mesa de pool', 'juego electrónico', 'russia block', 'tarjeta flash', 'didáctico']):
        return 'Juegos de Mesa'
    if any(x in n for x in ['alfombra', 'piso didáctico']):
        return 'Juegos de Mesa'
    if any(x in n for x in ['peluche', 'llavero', 'cartera', 'maquina saca', 'máquina saca', 'muñeco']):
        return 'Peluches y Accesorios'
    if any(x in n for x in ['decoración', 'decoration']):
        return 'Hogar y Decoración'
    if any(x in n for x in ['lego', 'magnético', 'magnetico', 'construcción']):
        return 'Construcción'
    if any(x in n for x in ['gatito labubu', 'auriculares gato']):
        return 'Audio'
    return 'Otros'

# 5. Build new products list
new_products = []
for idx, pdf_p in enumerate(pdf_products):
    prod_id = idx + 1
    
    existing = current_by_page.get(pdf_p['page'], None)
    wholesale = existing['wholesale'] if existing and 'wholesale' in existing else []
    
    category = get_category(pdf_p['name'])
    if existing and existing.get('category') and category == 'Otros':
        category = existing['category']
    
    img = find_image(pdf_p['name'])
    
    product = {
        'id': prod_id,
        'name': pdf_p['name'],
        'price': pdf_p['price'],
        'priceNum': pdf_p['priceNum'],
        'wholesale': wholesale,
        'category': category,
        'page': pdf_p['page'],
    }
    
    if img:
        product['img'] = img
    
    new_products.append(product)

# 6. Output
output = {
    'products': new_products,
    'categories': sorted(set(p['category'] for p in new_products)),
    'catEmoji': {
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
        'Vehículos': '🏎️'
    }
}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

with_img = sum(1 for p in new_products if 'img' in p)
without_img = sum(1 for p in new_products if 'img' not in p)
print(f"JSON actualizado: {len(new_products)} productos, {with_img} con imagen, {without_img} sin imagen")

if without_img > 0:
    print("\nProductos sin imagen:")
    for p in new_products:
        if 'img' not in p:
            print(f"  - {p['name']} (${p['price']})")
