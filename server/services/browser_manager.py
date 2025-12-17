"""
shared browser instance manager for Playwright.
maintains a single browser instance to reduce memory and startup time.
"""
import asyncio
from playwright.async_api import async_playwright, Browser, Playwright

# global state
_playwright: Playwright = None
_browser: Browser = None
_lock = asyncio.Lock()

# memory-optimized browser args
BROWSER_ARGS = [
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-sync',
    '--disable-translate',
    '--no-first-run',
    '--disable-features=site-per-process',
    '--js-flags=--max-old-space-size=256',
    '--renderer-process-limit=1',
    '--disable-software-rasterizer',
]


async def get_browser() -> Browser:
    """
    get the shared browser instance.
    creates one if it doesn't exist (lazy init)
    """
    global _playwright, _browser
    
    async with _lock:
        if _browser is None or not _browser.is_connected():
            print("[browser_manager] | launching shared playwright browser...")
            _playwright = await async_playwright().start()
            _browser = await _playwright.chromium.launch(
                headless=True,
                args=BROWSER_ARGS
            )
            print("[browser_manager] | shared browser ready")
        return _browser


async def close_browser():
    """
    cleanup browser on shutdown.
    called from FastAPI lifespan.
    """
    global _playwright, _browser
    
    async with _lock:
        if _browser:
            print("[browser_manager] | closing shared playwright browser...")
            await _browser.close()
            _browser = None
        if _playwright:
            await _playwright.stop()
            _playwright = None
            print("[browser_manager] | browser manager stopped")
