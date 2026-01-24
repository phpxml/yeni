import requests
import sys

def get_live_link():
    # Show Max API adresi
    api_url = "https://moe.showtv.com.tr/v1/content/showmax?type=live"
    
    # Tarayiciyi tam taklit eden basliklar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.showmax.com.tr/",
        "Origin": "https://www.showmax.com.tr",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    session = requests.Session()
    
    try:
        # Once ana sayfaya bir istek atip cerez (cookie) alalim
        session.get("https://www.showmax.com.tr/canli-yayin", headers=headers, timeout=15)
        
        # Simdi asil API istegini yapalim
        response = session.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            m3u8_link = data.get('data', {}).get('media', {}).get('link', {}).get('hls')
            return m3u8_link
        else:
            # Hata kodunu GitHub loglarina basar
            print(f"Hata: Sunucu {response.status_code} cevabi verdi.", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Baglanti Hatasi: {str(e)}", file=sys.stderr)
        return None

if __name__ == "__main__":
    link = get_live_link()
    if link:
        # Dosya formatini olustur
        print("#EXTM3U")
        print("#EXTINF:-1,Show Max")
        print(link)
    else:
        # Link yoksa KIRMIZI yanmasini sagla
        sys.exit(1)
