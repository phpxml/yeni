
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': '[https://www.showtv.com.tr/](https://www.showtv.com.tr/)'
    }
    try:
        response = requests.get(url, verify=False, timeout=15, headers=headers)
        match = re.search(r'https?://[^\s"\']+\.m3u8', response.text)
        return match.group(0) if match else None
    except:
        return None

def main():
    channels = [
        {
            "name": "Show TV",
            "url": "[https://www.showtv.com.tr/canli-yayin](https://www.showtv.com.tr/canli-yayin)",
            "logo": "[https://mo.ciner.com.tr/showtv/assets/images/logo-show-tv.png](https://mo.ciner.com.tr/showtv/assets/images/logo-show-tv.png)",
            "backup": "[https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8](https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8)"
        },
        {
            "name": "Show Turk",
            "url": "[https://www.showturk.com.tr/canli-yayin](https://www.showturk.com.tr/canli-yayin)",
            "logo": "[https://mo.ciner.com.tr/showtv/assets/images/logo-show-turk.png](https://mo.ciner.com.tr/showtv/assets/images/logo-show-turk.png)",
            "backup": "[https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8](https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8)"
        },
        {
            "name": "Show Max",
            "url": "[https://www.showmax.com.tr/canli-yayin](https://www.showmax.com.tr/canli-yayin)",
            "logo": "[https://mo.ciner.com.tr/showmax/assets/images/logo-show-max.png](https://mo.ciner.com.tr/showmax/assets/images/logo-show-max.png)",
            "backup": "[https://ciner-live.ercdn.net/showmax/showmax_720p.m3u8](https://ciner-live.ercdn.net/showmax/showmax_720p.m3u8)"
        },
        {
            "name": "Haberturk",
            "url": "[https://www.haberturk.com/canli-yayin](https://www.haberturk.com/canli-yayin)",
            "logo": "[https://mo.ciner.com.tr/haberturk/assets/images/logo-haberturk-tv.png](https://mo.ciner.com.tr/haberturk/assets/images/logo-haberturk-tv.png)",
            "backup": "[https://ciner-live.ercdn.net/haberturktv/haberturktv_720p.m3u8](https://ciner-live.ercdn.net/haberturktv/haberturktv_720p.m3u8)"
        }
    ]

    print("#EXTM3U")
    for ch in channels:
        stream_url = get_link(ch["url"]) or ch["backup"]
        print(f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-logo="{ch["logo"]}",{ch["name"]}')
        print(stream_url)

if __name__ == "__main__":
    main()
