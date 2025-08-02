import re
from difflib import SequenceMatcher
from models.hotel import *
from rapidfuzz import fuzz

def encontrar_mejor_match(nombre_excel, nombres_web):
    nombre_excel_n = normalizar(nombre_excel)
    mejor_match = None
    mejor_score = 0.0

    for nombre_web in nombres_web:
        nombre_web_n = normalizar(nombre_web)

        # Score por Levenshtein/SequenceMatcher
        ratio = calcular_ratio_similitud(nombre_excel_n, nombre_web_n)

        # Score por palabras en común (Jaccard)
        palabras_excel = set(nombre_excel_n.split())
        palabras_web = set(nombre_web_n.split())
        interseccion = len(palabras_excel & palabras_web)
        union = len(palabras_excel | palabras_web)
        jaccard_score = interseccion / union if union else 0

        # Score combinado
        score_total = (ratio + jaccard_score) / 2

        if score_total > mejor_score:
            mejor_score = score_total
            mejor_match = nombre_web

    return mejor_match, mejor_score

def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)  # eliminar puntuación
    palabras = texto.split()
    palabras.sort()  # ordenar alfabéticamente
    return ' '.join(palabras)

def calcular_ratio_similitud(a, b):
    return SequenceMatcher(None, a, b).ratio()

def obtener_mejor_match_con_breakfast(combo_elegido, hab_web):
    # Normalizar combo_elegido
    tiene_breakfast = contiene_breakfast(combo_elegido)
    print(tiene_breakfast)
    # Extraer nombres de habitaciones web
    nombres_web = [habitacion.nombre for habitacion in hab_web]

    # Buscar mejor match de nombre
    mejor_nombre, _ = encontrar_mejor_match(combo_elegido, nombres_web)
    print("MEJOR NOMBRE WEB ",mejor_nombre)
    print("COMBO ELEGIDO",combo_elegido)
    for habitacion in hab_web:
        if habitacion.nombre == mejor_nombre:
            
            if tiene_breakfast:
                # Filtrar combos que tengan algún indicio de breakfast en el título
                combos_filtrados = [
                    combo for combo in habitacion.combos
                    if contiene_breakfast(combo.titulo)
                ]
                if combos_filtrados:
                    # Retorna la misma habitación, pero con los combos filtrados
                    return Habitacion(
                        nombre=habitacion.nombre,
                        detalles=habitacion.detalles,
                        combos=combos_filtrados
                    )
                else:
                    return None  # No hay combos que coincidan con breakfast
            else:
                return habitacion  # No requiere filtrado
    return None

def contiene_breakfast(texto, umbral=75):
    texto_norm = texto.lower()
    patrones_relacionados = [
        "w/breakfast", "with breakfast", "includes breakfast",
        "breakfast inclusive", "breakfast included"
    ]
    print(f"[DEBUG entrada] contiene_breakfast con texto_norm={texto_norm!r}")

    # primero chequeo directo rápido
    for patron in patrones_relacionados:
        if patron in texto_norm:
            return True

    # luego fuzzy partial (subcadena)
    for patron in patrones_relacionados:
        ratio = fuzz.partial_ratio(texto_norm, patron)
        print(f"[DEBUG fuzzy] '{patron}' vs texto -> partial_ratio = {ratio}")
        if ratio >= umbral:
            return True

    return False



##################### DE MOMENTO SIN UTILIDAD #########################
##### utilizada por encontrar mejor match, no tiene en cuenta combos#####
def obtener_mejor_match(combo_elegido,hab_web):
   
    # Obtener el nombre del combo de Excel
     # o combo_elegido["nombre"] si es un dict

    # Extraer los nombres de habitaciones web
    nombres_web = [habitacion.nombre for habitacion in hab_web]

    # Obtener el mejor nombre match y su score
    mejor_nombre, _ = encontrar_mejor_match(combo_elegido, nombres_web)

    # Buscar el objeto habitación web correspondiente a ese nombre
    for habitacion in hab_web:
        if habitacion.nombre == mejor_nombre:
            return habitacion

    return None  

def contiene_breakfast_exp_reg(texto):
    texto_norm = texto.lower()
    patrones = [
        r"w/?breakfast",           # w/breakfast o wbreakfast
        r"with breakfast",
        r"includes breakfast",
        r"breakfast inclusive",
        r"breakfast included",     # variante útil
    ]
    for pat in patrones:
        if re.search(pat, texto_norm):
            return True
    return False
###############################################