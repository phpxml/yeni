import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_stream():
    target_url = "[https://www.showturk.com.tr/canli-yayin](https://www.showturk.com.tr/canli-yayin)"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': '[https://www.showturk.com.tr/](https://www.showturk.com.tr/)'
    }

    try:
        response = requests.get(target_url, verify=False, timeout=20, headers=headers)
        match = re.search(r'https?://[^\s"\']+/showturk/[^\s"\']+\.m3u8', response.text)

        print("#EXTM3U")
        if match:
            m3u8_url = match.group(0)
            print('#EXTINF:-1 tvg-id="ShowTurk" tvg-logo="[https://mo.ciner.com.tr/showtv/assets/images/logo-show-turk.png](https://mo.ciner.com.tr/showtv/assets/images/logo-show-turk.png)",Show Turk')
            print(m3u8_url)
        else:
            print('#EXTINF:-1,Show Turk')
            print("[https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8](https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8)")

    except:
        print("#EXTM3U")
        print('#EXTINF:-1,Show Turk')
        print("[https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8](https://ciner-live.ercdn.net/showturk/showturk_720p.m3u8)")

if __name__ == "__main__":
    get_stream()
