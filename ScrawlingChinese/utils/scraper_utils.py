import json
import os
from typing import List, Set, Tuple
from urllib.parse import urlencode

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
from datetime import date
from models.hotel import *



def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=True,  # Whether to run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.

    Returns:
        LLMExtractionStrategy: The settings for how to extract data using LLM.
    """
    # https://docs.crawl4ai.com/api/strategies/#llmextractionstrategy
   
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",  # Name of the LLM provider
        api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        schema=Habitacion.model_json_schema(),  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=(
        "Extrae una habitación con su nombre, su detalle, "
        "y una lista de promociones con su titulo (ejemplo 'desayuno incluido', 'cancelación gratuita', etc.),"
        "descripcion y precio por noche "
        ),  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        verbose=True,  # Enable verbose logging
    )

def fechas_validas(fecha_entrada: date, fecha_salida: date) -> bool:
    hoy = date.today()
    if fecha_entrada < hoy:
        print(f"Fecha de entrada {fecha_entrada} es anterior a hoy {hoy}.")
        return False
    if fecha_salida <= fecha_entrada:
        print(f"Fecha de salida {fecha_salida} debe ser posterior a la entrada {fecha_entrada}.")
        return False
    return True

async def procesar_resultado_scraping(result):
    if not (result.success and result.extracted_content):
        print(f"Error en la obtención: {result.error_message}")
        return None

    hotel_data = json.loads(result.extracted_content)

    # Verifico si LLM devolvió habitaciones
    if not hotel_data.get("habitacion"):
        print(" No se encontraron habitaciones disponibles según extracción LLM.")
        # Complemento con chequeo en HTML crudo
        if "no availability" in result.cleaned_html.lower() or "no rooms available" in result.cleaned_html.lower():
            print("Confirmado: no hay disponibilidad según contenido HTML.")
        else:
            print("Atención: no hay habitaciones extraídas, pero no se detectó mensaje explícito de no disponibilidad en HTML.")
        return None

    # Si hay habitaciones, devolver objeto Hotel o procesar más
    return Hotel(**hotel_data)



async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    base_url: str,
    params: dict,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    nombre_hotel: str = "Alvear Palace Hotel"
) -> Optional[Hotel]:
    
    url_completa = f"{base_url}?{urlencode(params)}"
    print(f"Loading hotel page: {url_completa}...")

    #ejecuta el crawl
    result = await crawler.arun(
        url=url_completa,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=llm_strategy,
            css_selector=css_selector,
            session_id=session_id,
        ),
    )
 
    if not (result.success and result.extracted_content):
        print(f"Error fetching hotel page: {result.error_message}")
        return None

##aca tendriamos que chequear validez de datos

    try:
        
        habitaciones_data = json.loads(result.extracted_content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

    if not habitaciones_data:
        print("No se encontraron habitaciones.")
        return None

    ### Si hubo habitaciones
    print(f"Se extrajeron {len(habitaciones_data)} habitaciones.")
    
    habitaciones = []
    for h in habitaciones_data:
        try:
            habitacion = Habitacion(**h)
            habitaciones.append(habitacion)
        except Exception as e:
            print(f"Error procesando una habitación: {e}")
            continue
    
    hotel = Hotel(
        detalles=nombre_hotel,
        habitacion=habitaciones
    )
    #imprimir_hotel(hotel)

    return hotel

def imprimir_hotel(hotel: Hotel):
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