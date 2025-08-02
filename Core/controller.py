from .gestor_datos import *


gestor = GestorDatos("./Data/Extracto.xlsx")

def dar_habitaciones_excel():
    return gestor.habitaciones_excel




