from .gestor_datos import *


gestor = GestorDatos("./Data/Extracto.xlsx")

def dar_hoteles_excel():
    return gestor.hoteles_excel_get

def dar_habitaciones_excel(hotelExcel, tipo):
    return gestor.habitaciones_excel_get(hotelExcel, tipo)

def dar_tipos_habitacion_excel(HotelExcel):
    return gestor.tipos_habitaciones_excel_get(HotelExcel)

## Tiene que estar todo el proceso para realizar la comparación
def comparar_habitaciones(habitacion_excel,precio_hab_excel):
    gestor.coincidir_excel_web(habitacion_excel) #busca la mejor coincidencia con hab web
    precio_web = gestor.mejor_habitacion_web_get
    ##precio_web = gestor.mejor_habitacion_web.combos[0].precio # type: ignore
    ##precio_combo_elegido = precio_hab_excel # type: ignore
    diferencia = abs(precio_hab_excel - precio_web) # type: ignore
    if diferencia>1:   # type: ignore
        return False
    else:
        return True
    

def dar_habitacion_web():
    return gestor.mejor_habitacion_web_get

async def dar_hotel_web(fecha_ingreso,fecha_egreso,adultos,niños):

    hotel = await gestor.obtener_hotel_web( fecha_ingreso,fecha_egreso,adultos,niños)

    return hotel


