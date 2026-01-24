import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_live_link():
    url = "[https://www.showtv.com.tr/canli-yayin](https://www.showtv.com.tr/canli-yayin)"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': '[https://www.showtv.com.tr/](https://www.showtv.com.tr/)'
    }
    try:
        response = requests.get(url, verify=False, timeout=15, headers=headers)
        if response.status_code == 200:
            # Sayfa içindeki dinamik m3u8 linkini yakalar
            match = re.search(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
            if match:
                return match.group(0)
    except:
        pass
    return "[https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8](https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8)"

def main():
    link = get_live_link()
    print("#EXTM3U")
    print('#EXTINF:-1 tvg-id="Show TV" tvg-logo="[https://mo.ciner.com.tr/showtv/assets/images/logo-show-tv.png](https://mo.ciner.com.tr/showtv/assets/images/logo-show-tv.png)",Show TV')
    print(link)

if __name__ == "__main__":
    main()
