import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_token_link():
    url = "[https://www.showtv.com.tr/canli-yayin](https://www.showtv.com.tr/canli-yayin)"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': '[https://www.showtv.com.tr/](https://www.showtv.com.tr/)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        content = response.text
        # Show TV ulusal yayin icin m3u8 ve token yakalama
        match = re.search(r'(https?://[^\s"\']+/showtv\.m3u8\?e=[^\s"\']+)', content)
        if match:
            return match.group(1).replace("\\/", "/")
        return None
    except:
        return None

def main():
    token_link = get_token_link()
    
    if token_link:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': '[https://www.showtv.com.tr/](https://www.showtv.com.tr/)'
        }
        try:
            res = requests.get(token_link, headers=headers, timeout=10, verify=False)
            if res.status_code == 200:
                base_url = "[https://ciner-live.ercdn.net/showtv/](https://ciner-live.ercdn.net/showtv/)"
                lines = res.text.splitlines()
                output = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("showtv"):
                        output.append(base_url + line)
                    else:
                        output.append(line)
                print("\n".join(output))
                return
        except:
            pass

    # Fail durumunda yedek link
    print("#EXTM3U")
    print("#EXT-X-STREAM-INF:BANDWIDTH=1200000,RESOLUTION=1280x720")
    print("[https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8](https://ciner-live.ercdn.net/showtv/showtv_720p.m3u8)")

if __name__ == "__main__":
    main()
