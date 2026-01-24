import os
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_live_stream():
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
        
        driver.get("https://www.showtv.com.tr/canli-yayin")
        time.sleep(30) 

        found_url = None
        for request in driver.requests:
            if request.response:
                if ".m3u8" in request.url and "ciner" in request.url:
                    found_url = request.url
                    break
        
        driver.quit()
        return found_url
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    stream_url = get_live_stream()
    if stream_url:
        with open("showtv.m3u8", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1,Show TV\n")
            f.write(stream_url)
        print("Success: File updated.")
    else:
        print("Failed: URL not found.")
