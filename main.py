import asyncio
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def extract_url(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                java_script_enabled=True
            )
            page = await context.new_page()
            await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => undefined })""")

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=120000)
                logger.info("App has started.")
                logger.info("Accessing link now!!")
                await page.wait_for_selector("video[src]", timeout=120000)
                html = await page.inner_html("body")
            except Exception as e:
                print(f"[!] Page interaction error: {e}")
                return None
            finally:
                await context.close()
                await browser.close()

            tree = HTMLParser(html)
            node = tree.css("video")
            logger.info("Got it!!")
            return node[0].attributes.get("src") if node else None

    except Exception as e:
        print(f"[!] Browser error: {e}")
        return None

# test
if __name__=="__main__":
    async def main():
        url = await extract_url("https://www.threads.com/@hbaservices/post/DKejYDZizFW/media")
        print(url)

    asyncio.run(main())
