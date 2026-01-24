import requests
import sys

def get_live_link():
    # Show Max'in link ürettiği gerçek API adresi
    api_url = "https://moe.showtv.com.tr/v1/content/showmax?type=live"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.showmax.com.tr/",
        "Origin": "https://www.showmax.com.tr"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=20)
        # Hata kodunu kontrol et
        if response.status_code == 200:
            data = response.json()
            m3u8_link = data.get('data', {}).get('media', {}).get('link', {}).get('hls')
            return m3u8_link
        else:
            sys.stderr.write(f"API Hatasi: Kod {response.status_code}\n")
            return None
    except Exception as e:
        sys.stderr.write(f"Baglanti Hatasi: {str(e)}\n")
        return None

if __name__ == "__main__":
    link = get_live_link()
    if link:
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(link)
    else:
        sys.exit(1)
