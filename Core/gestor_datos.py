from ExtractorDatos.extractor import *
from ScrawlingChinese.crawler import *
from models.hotel import *
from Core.comparador import *
import pickle
import os

class GestorDatos:
    def __init__(self,path_excel):
        self.__path = path_excel
        self.__datos_excel = cargar_excel(self.__path) 
        # self.tipos_habitacion_excel = obtener_tipos_habitacion(self.__path) DE MOMENTO NO SE USAo
        # self.__habitaciones_excel = self.__datos_excel.habitaciones
        #[HabitacionExcel.nombre for HabitacionExcel in self.__datos_excel.habitaciones]
        self.__hotel_web : Optional[Hotel] = None
        self.__habitaciones_web : Optional[List[Habitacion]] = None
        # self.__combo_elegido = self.__habitaciones_excel[0].nombre #hardcodeado
        # self.__precio_combo_elegido = self.__habitaciones_excel[0].precio #hardcodeado
        self.mejor_habitacion_web : Habitacion | None
    
    def coincidir_excel_web (self, habitacion_excel):
        self.mejor_habitacion_web = obtener_mejor_match_con_breakfast(habitacion_excel, self.__habitaciones_web)
        if self.mejor_habitacion_web is None:
            raise ValueError(f"[ERROR] No se encontró una coincidencia para el combo: {self.__combo_elegido}")
        return 

    async def obtener_hotel_web(self, fecha_ingreso,fecha_egreso,adultos,niños):
        if os.path.exists("hotel_guardado.pkl"):
            with open("hotel_guardado.pkl", "rb") as f:
                self.__hotel_web = pickle.load(f)
                # imprimir_hotel(self.__hotel_web)
                self.__habitaciones_web = self.__hotel_web.habitacion
        else:
            self.__hotel_web = await crawl_alvear(fecha_ingreso, fecha_egreso, adultos, niños)  
            with open("hotel_guardado.pkl", "wb") as f:
                pickle.dump(self.__hotel_web, f)
                # imprimir_hotel(self.__hotel_web)
                self.__habitaciones_web = self.__hotel_web.habitacion
        return self.__hotel_web
    
    @property
    def hoteles_excel_get(self)-> List[HotelExcel]:
        return self.__datos_excel.hoteles
    
    @property
    def tipos_habitaciones_excel_get(self,hotelExcel)-> List[TipoHabitacionExcel] | None:
        for hotel in self.__datos_excel.hoteles:
            if hotel.nombre == hotelExcel:
                return hotel.tipos
            else:
                return "no se encontro el hotel"
    
    @property
    def habitaciones_excel_get(self,hotelExcel,tipo = None)-> List[HabitacionExcel] | None:
        if tipo is None:
            for hotel in self.__datos_excel.hoteles:
                if hotel.nombre == hotelExcel:
                    return hotel.habitaciones_directas
                else:
                    print("no se encontro el hotel")
        else:
            for hotel in self.__datos_excel.hoteles:
                if hotel.nombre == hotelExcel:
                    for tipos in hotel.tipos:
                        if tipos.nombre == tipo:
                            return tipos.habitaciones
                else:
                    print("no se encontro el tipo del hotel")
        return None
        
    
    # @property
    # def precio_combo_elegido_get(self)-> float:
    #     return self.__precio_combo_elegido

    @property
    def mejor_habitacion_web_get(self)-> Habitacion | None:
        return self.mejor_habitacion_web    

################## IMPRESIONES ###############
# def imprimir_hotel(hotel):
#     print(f"\n🏨 Hotel: {hotel.detalles}")
#     print("=" * (8 + len(hotel.detalles)))

#     for i, habitacion in enumerate(hotel.habitacion, start=1):
#         print(f"\n🛏️ Habitación {i}: {habitacion.nombre}")
#         if habitacion.detalles:
#             print(f"   📋 Detalles: {habitacion.detalles}")
        
#         if habitacion.combos:
#             print("   💼 Combos:")
#             for combo in habitacion.combos:
#                 print(f"     🔹 {combo.titulo}")
#                 print(f"        📃 {combo.descripcion}")
#                 print(f"        💵 ${combo.precio:.2f}")
#         else:
#             print("   ❌ Sin promociones registradas.")   


## ORDEN
# obtener hotel web 
# coincidir excel web
# luego comparar precios