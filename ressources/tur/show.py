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
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get("https://www.showtv.com.tr/canli-yayin")
        time.sleep(20) 

        for request in driver.requests:
            if request.response:
                if ".m3u8" in request.url and "ciner" in request.url:
                    return request.url
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
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
