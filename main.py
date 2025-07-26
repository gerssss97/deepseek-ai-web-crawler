import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
# from utils.data_utils import (
#     save_venues_to_csv,
# )
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_venues():
    """
    Main function to crawl venue data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "venue_crawl_session"

    # Initialize state variables
    params_busqueda = {
        "adult": 2,
        "child": 0,
        "arrive": "2025-07-12",
        "depart": "2025-07-13",
        "chain": 24447,
        "hotel": 6933,
        "currency": "USD",
        "level": "hotel",
        "locale": "en-US",
        "productcurrency": "USD",
        "rooms": 1,
        "src": 30,
    }

    # Start the web crawler context
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
    
        # Fetch and process data from the current page
        hotel = await fetch_and_process_page(
            crawler,
            BASE_URL,
            params_busqueda,
            CSS_SELECTOR,
            llm_strategy,
            session_id,
        )


    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_venues()


if __name__ == "__main__":
    asyncio.run(main())
