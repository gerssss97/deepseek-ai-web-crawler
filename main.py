from Core.gestor_datos import *

if __name__ == "__main__":
    async def main():
        gestor = GestorDatos("./Data/Extracto.xlsx")
        gestor.mostrar_combos_excel()  # Esta es síncrona, se puede llamar directamente

        # Llamada a función asíncrona y se espera a que termine
        # await gestor.obtener_hotel_web("2025-07-15", "2025-07-17", 2, 0)

        # # Luego de que terminó la anterior, llamamos a la siguiente
        # gestor.coincidir_excel_web()  # Esta suponemos que es sincrónica, si no avisame

    asyncio.run(main())