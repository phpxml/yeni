import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Tarayıcıyı aç
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Network trafiğini dinle
        token_link = ""
        def handle_request(request):
            nonlocal token_link
            if "wmsAuthSign" in request.url:
                token_link = request.url

        page.on("request", handle_request)
        
        # Siteye git
        print("Site açılıyor...")
        await page.goto("https://www.elahmad.com/tv/canli-tv-live.php")
        await asyncio.sleep(15) # JS'nin çalışması için bekle
        
        if token_link:
            print(f"Buldum: {token_link}")
            with open("liste.m3u", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1, Star TV\n{token_link}")
        else:
            print("Link yakalanamadı.")

        await browser.close()

asyncio.run(run())
