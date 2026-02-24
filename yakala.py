import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Tarayıcıyı açıyoruz
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Ahmet'in sitesine gidiyoruz
        url = "https://www.elahmad.com/tv/live/channels.php?id=83"
        print(f"Siteye gidiliyor: {url}")
        
        # Linkleri yakalamak için ağ trafiğini dinliyoruz
        link = None
        def handle_request(request):
            nonlocal link
            if "m3u8" in request.url and "wmsAuthSign" in request.url:
                link = request.url

        page.on("request", handle_request)
        page.goto(url)
        
        # Sayfanın ve JavaScript'in yüklenmesi için 10 saniye bekliyoruz
        page.wait_for_timeout(10000)
        
        if link:
            print(f"Başarılı! Link yakalandı: {link}")
            with open("liste.m3u", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1, Star TV\n{link}")
        else:
            print("Link yakalanamadı.")
            
        browser.close()

if __name__ == "__main__":
    run()
