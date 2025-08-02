from ExtractorDatos.extractor import *
from ScrawlingChinese.crawler import *
from models.hotel import *
from Core.comparador import *
import pickle
import os

class GestorDatos:
    hotel: Optional[Hotel]
    
    def __init__(self,path_excel):
        self.path = path_excel
        self.tipos_habitacion_excel= obtener_tipos_habitacion(self.path)
        self.habitaciones_excel = obtener_habitaciones_excel(self.path)
        self.precios_excel= obtener_precios_excel(self.path) 
        self.hotel : Optional[Hotel] = None
        self.hab_web = None
        self.combo_elegido = self.habitaciones_excel[2]
        self.precio_combo_elegido= self.habitaciones_excel[4]

    def mostrar_tipos_habitacion_excel(self):
        try:
            suites = obtener_tipos_habitacion(self.path)
            print("Tipos de habitaciones encontradas:")
            for suite in suites:
                print(f" - {suite}")
        except Exception as e:
            print(f"[ERROR] No se pudieron obtener los tipos de habitaciones: {e}")
            
    def mostrar_habitaciones_excel(self):
        try:
            habitaciones = obtener_habitaciones_excel(self.path)
            print("Habitaciones encontradas:")
            for hab in habitaciones:
                print(f" - {hab}")
         
        except Exception as e:
            print(f"[ERROR] No se pudieron obtener las habitaciones : {e}")
            
    def coincidir_excel_web (self):
        mejor_habitacion_web = obtener_mejor_match_con_breakfast(self.combo_elegido, self.hab_web)
        imprimir_habitacion(mejor_habitacion_web)
        print("COMBO ELEGIDO",self.combo_elegido)
        return mejor_habitacion_web

    async def obtener_hotel_web(self, fecha_ingreso,fecha_egreso,adultos,niños):
       
        if os.path.exists("hotel_guardado.pkl"):
            with open("hotel_guardado.pkl", "rb") as f:
                self.hotel = pickle.load(f)
                imprimir_hotel(self.hotel)
                self.obtener_nombres_hab_web()
        else:
            self.hotel = await crawl_alvear(fecha_ingreso, fecha_egreso, adultos, niños)  
            with open("hotel_guardado.pkl", "wb") as f:
                pickle.dump(self.hotel, f)
                imprimir_hotel(self.hotel)
                self.obtener_nombres_hab_web()
        return 
         
         
    def obtener_nombres_hab_web(self):
        if self.hotel is None:
            raise ValueError("El hotel aún no fue cargado. Llamá a crawl_alvear primero.")
        self.hab_web = self.hotel.habitacion
      
        #print(self.hab_web)
        return

    def comparar_precio(self):
        pass




################## IMPRESIONES ###############
def imprimir_hotel(hotel):
    print(f"\n🏨 Hotel: {hotel.detalles}")
    print("=" * (8 + len(hotel.detalles)))

    for i, habitacion in enumerate(hotel.habitacion, start=1):
        print(f"\n🛏️ Habitación {i}: {habitacion.nombre}")
        if habitacion.detalles:
            print(f"   📋 Detalles: {habitacion.detalles}")
        
        if habitacion.combos:
            print("   💼 Combos:")
            for combo in habitacion.combos:
                print(f"     🔹 {combo.titulo}")
                print(f"        📃 {combo.descripcion}")
                print(f"        💵 ${combo.precio:.2f}")
        else:
            print("   ❌ Sin promociones registradas.")   

def imprimir_habitacion(habitacion):
    print(f"\n🛏️ Habitación COINCIDENTE: {habitacion.nombre}")
    if habitacion.detalles:
        print(f"   📋 Detalles: {habitacion.detalles}")
    
    if habitacion.combos:
        print("   💼 Combos:")
        for combo in habitacion.combos:
            print(f"     🔹 {combo.titulo}")
            print(f"        📃 {combo.descripcion}")
            print(f"        💵 ${combo.precio:.2f}")
    else:
        print("   ❌ Sin promociones registradas.")   

