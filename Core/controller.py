from .gestor_datos import *


gestor = GestorDatos("./Data/Extracto.xlsx")

def dar_habitaciones_excel():
    return gestor.habitaciones_excel

## Tiene que estar todo el proceso para realizar la comparación
def comparar_habitaciones(habitacion_excel,precio_hab_excel):
    gestor.coincidir_excel_web()
    precio_web = gestor.mejor_habitacion_web.combos[0].precio # type: ignore
    diferencia = abs(gestor.precio_combo_elegido - precio_web) # type: ignore
    if diferencia>1:   # type: ignore
        return False
    else:
        return True
    
def dar_habitacion_web():
    return gestor.mejor_habitacion_web_get

async def dar_habitacion_web(fecha_ingreso,fecha_egreso,adultos,niños):
    print("dar habitacion web")
    hotel= await gestor.obtener_hotel_web( fecha_ingreso,fecha_egreso,adultos,niños)
    
    return hotel


