import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_token_link():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        driver.get("https://www.showmax.com.tr/canli-yayin")
        time.sleep(30) # Token'ın oluşması için gereken süre

        found_url = None
        for request in reversed(driver.requests):
            if request.response:
                if ".m3u8" in request.url and "ciner" in request.url:
                    found_url = request.url
                    break
        
        driver.quit()
        return found_url
    except Exception as e:
        return None

if __name__ == "__main__":
    final_link = get_token_link()
    if final_link:
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(final_link)
        sys.stdout.flush()
    else:
        sys.exit(1) # Link bulunamazsa hata kodu ver
