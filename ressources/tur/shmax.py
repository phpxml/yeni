import requests
import sys

def get_live_link():
    api_url = "https://moe.showtv.com.tr/v1/content/showmax?type=live"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.showmax.com.tr/",
        "Origin": "https://www.showmax.com.tr"
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # API'den gelen m3u8 linkini aliyoruz
            return data.get('data', {}).get('media', {}).get('link', {}).get('hls')
    except:
        return None
    return None

if __name__ == "__main__":
    link = get_live_link()
    if link:
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(link)
    else:
        # Link yoksa hata ver ki GitHub bizi uyarsin
        sys.exit(1)
