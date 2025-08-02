from openpyxl import load_workbook
import string
from models.hotel import *

#incluirla en una nueva funcion
def obtener_tipos_habitacion(path_excel):
    wb = load_workbook(path_excel)
    ws = wb.active # type: ignore

    tipos_habitacion = []
    for i, row in enumerate(ws.iter_rows(values_only=True,max_row=25)): # type: ignore
       
        if not any(row):
            continue  # fila vacía, la ignoramos
        
        if row[0] is None:
            continue    # primer campo vacio, lo ignoramos
       
        nombre = str(row[0]).strip().lower()
        col_precio = row[2]

        exclusiones = ["season rates", "(per room)", "alvear palace","closing agreement",
                       "rates includes","promotion","not included"]
        
        #si esta en alguna de las exclusiones, ignoro
        if any(nombre.startswith(excl) for excl in exclusiones):
            continue
        
        
        #si no tiene precio, ignoro
        if col_precio is not None and str(col_precio).strip() != "":
            continue
        
        nombre = nombre.rstrip(string.punctuation + " ").strip()
        tipos_habitacion.append(nombre)

    return tipos_habitacion

##meterle que saque el precio tambien
def obtener_habitaciones_excel(path_excel):
    wb = load_workbook(path_excel)
    ws = wb.active # type: ignore

    combos = []
    for i, row in enumerate(ws.iter_rows(values_only=True,max_row=25)): # type: ignore
        if not any(row):
            continue  # fila vacía, la ignoramos
        
        if row[0] is None:
            continue    # primer campo vacio, lo ignoramos
       
        nombre = str(row[0]).strip().lower()
        col_precio = row[2]
        exclusiones = ["season rates", "(per room)", "alvear palace","closing agreement",
                       "rates includes","promotion","not included"]
        
        #si esta en alguna de las exclusiones, ignoro
        if any(nombre.startswith(excl) for excl in exclusiones):
            continue
        
        if col_precio is None or str(col_precio).strip() == "":
            continue
        
        
        combos.append(nombre)
        
    return combos





EXCLUSIONES = [
    "season rates", "(per room)", "alvear palace", "closing agreement",
    "rates includes", "promotion", "not included"
]
def cargar_excel(path_excel, max_row=25) -> DatosExcel:
    wb = load_workbook(path_excel)
    ws = wb.active  # type: ignore

    entradas: list[HabitacionExcel] = []
    for i, row in enumerate(ws.iter_rows(values_only=True, max_row=max_row)):  # type: ignore
        if not any(row):
            continue  # fila vacía

        if row[0] is None:
            continue  # sin nombre

        nombre_raw = str(row[0])
        nombre_norm = nombre_raw.strip().lower()
        if any(nombre_norm.startswith(excl) for excl in EXCLUSIONES):
            continue  # excluido

        col_precio = row[2]
        precio_raw = None
        if col_precio is not None and str(col_precio).strip() != "":
            precio_raw = str(col_precio)

        entry = HabitacionExcel(
            nombre=nombre_raw,
            precio_raw=precio_raw,
            row_idx=i
        )
        entradas.append(entry)

    tipos = [e.nombre for e in entradas if e.precio is None]
    habitaciones_con_precio = [e for e in entradas if e.precio is not None]

    return DatosExcel(
        tipos_habitacion_excel=tipos,
        habitaciones=habitaciones_con_precio
    )