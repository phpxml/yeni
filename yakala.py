import os
from playwright.sync_api import sync_playwright

def link_kazima():
    with sync_playwright() as p:
        # Gerçek bir tarayıcı açıyoruz (Tincat gibi)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        yakalanan_link = []

        # Sitenin arka planda yaptığı tüm istekleri dinle
        def request_izle(request):
            if "m3u8" in request.url and "wmsAuthSign" in request.url:
                yakalanan_link.append(request.url)

        page.on("request", request_izle)

        try:
            # Siteye giriş yap ve 15 saniye bekle (Sandbox'ın geçmesi için)
            page.goto("https://www.elahmad.com/tv/live/channels.php?id=83", wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(15000) 

            if yakalanan_link:
                final_link = yakalanan_link[0]
                with open("staryayin.m3u", "w", encoding="utf-8") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1, Star TV\n{final_link}")
                print(f"BAŞARILI: Link bulundu ve kaydedildi.")
            else:
                print("HATA: Link trafikten çekilemedi.")
        except Exception as e:
            print(f"HATA OLUŞTU: {e}")
        
        browser.close()

if __name__ == "__main__":
    link_kazima()
