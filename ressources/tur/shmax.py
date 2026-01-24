import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_link():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080") # Sayfayı tam boy açalım

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        driver.get("https://www.showmax.com.tr/canli-yayin")
        
        # Linki yakalamak için 45 saniye boyunca her 5 saniyede bir kontrol et
        found_url = None
        for _ in range(9): 
            time.sleep(5)
            for request in reversed(driver.requests):
                if request.response:
                    url = request.url.lower()
                    if ".m3u8" in url and "ciner" in url:
                        found_url = request.url
                        break
            if found_url:
                break
        
        driver.quit()
        return found_url
    except:
        return None

if __name__ == "__main__":
    live_url = get_link()
    
    # EĞER LİNK BULUNURSA YAZDIR
    if live_url:
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(live_url)
        sys.stdout.flush() # Veriyi hemen dosyaya gönder
    else:
        # Link bulunamazsa bile dosya boş kalmasın diye sabit bir mesaj yazdırabiliriz
        # Ya da hata verdirerek GitHub'ın KIRMIZI yanmasını sağlayalım ki durumu anla
        sys.stderr.write("Link yakalanamadı!\n")
        sys.exit(1) 
