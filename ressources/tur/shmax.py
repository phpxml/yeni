import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def yakala_yeni_link():
    # Tarayici ayarlarini yap
    options = Options()
    options.add_argument("--headless") # Ekran acilmadan arkada calisir
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Chrome surucusunu otomatik kur ve baslat
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Show Max canli yayin sayfasina gir
        driver.get("https://www.showmax.com.tr/canli-yayin")
        
        # Sayfanin ve en guncel tokenli linkin olusmasi icin bekle
        time.sleep(30) 

        guncel_link = None
        # Ag trafigini sondan basa tara (en son olusan tokenli m3u8 linkini bulur)
        for request in reversed(driver.requests):
            if request.response:
                # Show Max linkleri 'ciner' ve '.m3u8' icerir, icinde token (ex, st) bulunur
                if ".m3u8" in request.url and "ciner" in request.url:
                    guncel_link = request.url
                    break
        
        driver.quit()
        return guncel_link
    except:
        return None

if __name__ == "__main__":
    yeni_link = yakala_yeni_link()
    if yeni_link:
        # YML dosyanin '>' ile dosyaya yazmasi icin ciktiyi veriyoruz
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(yeni_link)
