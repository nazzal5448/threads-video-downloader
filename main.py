import asyncio
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser

async def extract_url(url):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False, args=["--no-sandbox"])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                java_script_enabled=True
            )
            page = await context.new_page()
            await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => undefined })""")

            try:
                await page.goto(url, wait_until="load", timeout=120000)
                print("Url Opened!!")
                await page.wait_for_selector("#barcelona-splash-screen", state="hidden", timeout=15000)
                await page.click("div.x1ey2m1c.x9f619.xds687c", timeout=90000)
                await page.mouse.click(30, 35, button="left")
                await page.click("body", timeout=0)
                await page.click("div.x1ey2m1c.x9f619.xds687c.x17qophe.x10l6tqk.x13vifvy.x1ypdohk")
                print("Accessing video link now!")
                await page.wait_for_selector("div.x1f7gzso.x1n2onr6.x87ps6o video.x1lliihq", timeout=12000)
                html = await page.inner_html("body")
            except Exception as e:
                print(f"[!] Page interaction error: {e}")
                return None
            finally:
                await context.close()
                await browser.close()

            tree = HTMLParser(html)
            node = tree.css("div.x1f7gzso.x1n2onr6.x87ps6o video.x1lliihq")
            print("Got it!!")
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
